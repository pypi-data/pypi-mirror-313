# coding: utf-8
"""
The process of merge data.

"""

import functools
import typing as t

import pandas as pd

from cp_core.config import logger
from cp_core.libs.core.filter import errors

from . import const, current_reading, date, potential
from .anko_ac import ac_reading_from_anko
from .feature import compare_interference_vol
from .udl1_ac import ac_reading_from_udl1


def validate_datatype(func):
    @functools.wraps(func)
    def wrapper(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        assert data_type in (
            const.CC_AC_READING,
            const.CC_DC_READING,
            const.CP_DC_READING,
            const.CP_AC_READING,
            const.CP_DC_OFF_READING,
        )
        return func(df, data_type)

    return wrapper


@validate_datatype
def filter_reading(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
    d = df.loc[df["Record Type"] == data_type]
    if len(d.index) < 1:
        raise errors.EmptyError(f"No data in {data_type}")
    return d


def filter_current_ac_reading(
    data: pd.DataFrame, start: str, area: float
) -> pd.DataFrame:
    """# 获取 Current AC reading"""
    try:
        d = filter_reading(data, const.CC_AC_READING)
        d = date.locate_time(d, first_time=start)
        d = current_reading.current_ac_reading(d, area=area)

        # remove duplicate value in a second
        d.drop_duplicates(subset=const.DATE_NAME, keep="first", inplace=True)
        return d
    except errors.EmptyError as e:
        logger.error(e)
        columns_names = [
            const.DATE_NAME,
            const.cAC,
            const.AC_CURRENT_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            const.RELAY_NAME,
        ]
        return pd.DataFrame(columns=columns_names)


def filter_data(
    data: pd.DataFrame,
    start: str,
    column_name: str,
    reading_func: t.Callable[[pd.DataFrame], pd.DataFrame],
) -> pd.DataFrame:
    """根据头部、时间过滤数据。如果时间重叠了，只留下第一次出现的时间。"""
    pipeline = [
        lambda df: filter_reading(df, column_name),
        lambda df: date.locate_time(df, first_time=start),
        reading_func,
        lambda df: df.drop_duplicates(subset=const.DATE_NAME, keep="first"),
    ]
    d = data
    for fn in pipeline:
        d = fn(d)
    return d


def get_current_dc_reading(
    data: pd.DataFrame,
    start: str,
    area: float,
) -> pd.DataFrame:
    return filter_data(
        data,
        start,
        const.CC_DC_READING,
        lambda df: current_reading.current_dc_reading(df, area=area),
    )


def get_potential_dc_reading(data: pd.DataFrame, start: str) -> pd.DataFrame:
    return filter_data(
        data,
        start,
        const.CP_DC_READING,
        potential.potential_dc_reading,
    )


def filter_potential_ac_reading(data: pd.DataFrame, start: str) -> pd.DataFrame:
    try:
        df = filter_reading(data, const.CP_AC_READING)
        # d = trans_data(d)
        df = date.locate_time(df, first_time=start)
        df = potential.potential_ac_reading(df)
        df.drop_duplicates(subset=const.DATE_NAME, keep="first", inplace=True)
        return df
    except errors.EmptyError as e:
        # return an empty data frame
        logger.error(e)
        column_names = [
            const.DATE_NAME,
            const.pAC,
            const.AC_VOL_NAME,
            const.RELAY_NAME,
        ]

        return pd.DataFrame(columns=column_names)


def get_dc_data(udl2_data: pd.DataFrame, area: float) -> t.Tuple[pd.DataFrame, bool]:
    """

    Parameters
    ----------
    udl2_data :
    area :

    Returns
    -------

    """
    start = date.get_first_time(udl2_data)

    # remove redundant element
    # 删除冗余元素
    current_dc_df = get_current_dc_reading(udl2_data, start, area)
    potential_dc_df = get_potential_dc_reading(udl2_data, start)

    # potential_dc_df.to_csv("potential_dc_df.csv")

    if current_dc_df.empty and potential_dc_df.empty:
        columns_names = [
            const.DATE_NAME,
            const.POWER_ON_NAME,
            const.POLAR_NAME,
            const.DC_CURRENT_NAME,
            const.DC_CURRENT_DENSITY_NAME,
            const.RELAY_NAME,
        ]
        return pd.DataFrame(columns=columns_names), True

    # TODO[svtter]: problems with relay name.
    current_dc_df = current_dc_df.drop(const.cDC, axis=1)
    potential_dc_df = potential_dc_df.drop(const.pDC, axis=1)
    potential_dc_df = potential_dc_df.drop(const.RELAY_NAME, axis=1)

    merge_dc = pd.merge(
        left=potential_dc_df,
        right=current_dc_df,
        left_on=const.DATE_NAME,
        right_on=const.DATE_NAME,
    )
    # merge_dc
    return merge_dc, False


def assign_empty(data_from: pd.DataFrame, data_to: pd.DataFrame) -> pd.DataFrame:
    assert data_from.empty
    for col in data_from.head():
        if col in data_to.columns:
            continue
        data_to[col] = None
    return data_to


def merge_ac_dc(merged_ac: pd.DataFrame, merged_dc: pd.DataFrame) -> pd.DataFrame:
    if merged_ac.empty:
        merge_all = assign_empty(data_from=merged_ac, data_to=merged_dc)
    else:
        # 不使用 merged_dc 的 relay 列
        if const.RELAY_NAME in merged_dc.columns:
            merged_dc = merged_dc.drop(const.RELAY_NAME, axis=1)
        merge_all = pd.merge(
            left=merged_dc,
            right=merged_ac,
            left_on=const.DATE_NAME,
            right_on=const.DATE_NAME,
            how="outer",
        )

    merge_all.rename(columns={const.RELAY_NAME: const.STATUS_NAME}, inplace=True)
    return merge_all


def get_ac_data(
    df: pd.DataFrame, start: str, area: float
) -> t.Tuple[pd.DataFrame, bool]:
    """

    Parameters
    ----------
    data :
    start :
    area :

    Returns
    -------
    pd.DataFrame: ac data
    bool: is empty or not

    """
    current_ac_df = filter_current_ac_reading(df, start, area)
    potential_ac_df = filter_potential_ac_reading(df, start)
    if current_ac_df.empty and potential_ac_df.empty:
        columns_names = [
            const.DATE_NAME,
            const.AC_CURRENT_NAME,
            const.AC_VOL_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            const.RELAY_NAME,
        ]
        return pd.DataFrame(columns=columns_names), True

    # remove abundant elements
    potential_ac_df = potential_ac_df.drop(const.pAC, axis=1)
    potential_ac_df = potential_ac_df.drop(const.RELAY_NAME, axis=1)
    current_ac_df = current_ac_df.drop(const.cAC, axis=1)
    # c_ac_df = c_ac_df.drop(RELAY_NAME, axis=1)

    merged_ac = pd.merge(
        left=potential_ac_df,
        right=current_ac_df,
        left_on=const.DATE_NAME,
        right_on=const.DATE_NAME,
    )

    return merged_ac, False


def get_merge_data_from_udl2(df: pd.DataFrame, area: float) -> pd.DataFrame:
    """load data from udl2 data frame
    Parameters
    ----------
    data : origin data from udl2.csv
    area : piece area

    Returns
    -------

    """
    # 处理第一个数据，获取时间以及刷新时间
    df, start = date.str2datetime_first_time(df)

    merged_ac, ac_is_empty = get_ac_data(df=df, start=start, area=area)
    merged_dc, dc_is_empty = get_dc_data(udl2_data=df, area=area)

    if ac_is_empty and dc_is_empty:
        raise errors.EmptyError("no data in udl2 file")

    columns_names = [
        const.DATE_NAME,
        const.POWER_ON_NAME,
        const.POLAR_NAME,
        const.DC_CURRENT_NAME,
        const.DC_CURRENT_DENSITY_NAME,
        const.AC_CURRENT_NAME,
        const.AC_VOL_NAME,
        const.AC_CURRENT_DENSITY_NAME,
        const.STATUS_NAME,
    ]
    merged_all = merge_ac_dc(merged_ac, merged_dc)
    return merged_all.reindex(columns=columns_names)


def get_merge_data_from_anko(
    udl2_data: pd.DataFrame, anko_data: pd.DataFrame, area: float
) -> pd.DataFrame:
    udl2_data, start = date.str2datetime_first_time(udl2_data)

    # anko data
    potential_ac_df_anko = ac_reading_from_anko(anko_data, start)
    potential_ac_df_udl2 = filter_potential_ac_reading(udl2_data, start)

    if not potential_ac_df_udl2[const.AC_VOL_NAME].empty:
        potential_ac_df_anko[const.AC_VOL_NAME] = compare_interference_vol(
            potential_ac_df_anko, potential_ac_df_udl2
        )

    current_ac_df = filter_current_ac_reading(udl2_data, start, area)
    columns_names = [
        const.DATE_NAME,
        const.cAC,
        const.AC_CURRENT_NAME,
        const.AC_CURRENT_DENSITY_NAME,
        const.RELAY_NAME,
    ]
    assert columns_names == list(current_ac_df.head())

    # 去日期名称合并
    merged_ac = pd.merge(
        left=potential_ac_df_anko,
        right=current_ac_df,
        left_on=const.ANKO_DATE_NAME,
        right_on=const.DATE_NAME,
        how="outer",
    )
    merged_ac.drop(const.ANKO_DATE_NAME, axis=1)
    merged_ac = merged_ac[
        [
            const.DATE_NAME,
            const.AC_VOL_NAME,
            const.AC_CURRENT_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            const.RELAY_NAME,
        ]
    ]
    # merge_ac

    merged_dc, is_empty = get_dc_data(udl2_data=udl2_data, area=area)
    # merge_dc

    # 完全合并
    return merge_ac_dc(merged_ac, merged_dc)


def get_merge_data_from_udl1(
    udl2_data: pd.DataFrame, udl1_data: pd.DataFrame, area
) -> pd.DataFrame:
    udl2_data, start = date.str2datetime_first_time(data=udl2_data)

    # the special one
    potential_ac_df = ac_reading_from_udl1(udl1_data, start)
    current_ac_df = filter_current_ac_reading(udl2_data, start, area)
    potential_ac_df_udl2 = filter_potential_ac_reading(udl2_data, start)

    if not potential_ac_df_udl2[const.AC_VOL_NAME].empty:
        potential_ac_df[const.AC_VOL_NAME] = compare_interference_vol(
            potential_ac_df, potential_ac_df_udl2
        )

    columns_names = [
        const.DATE_NAME,
        const.cAC,
        const.AC_CURRENT_NAME,
        const.AC_CURRENT_DENSITY_NAME,
        const.RELAY_NAME,
    ]
    assert columns_names == list(current_ac_df.head())

    current_ac_df = current_ac_df.drop(const.cAC, axis=1)
    merged_ac = pd.merge(
        left=potential_ac_df,
        right=current_ac_df,
        left_on=const.UDL1_DATE_NAME,
        right_on=const.DATE_NAME,
        how="outer",
    )

    merged_ac.drop(const.UDL1_DATE_NAME, axis=1)

    # confirm column data
    columns_names = [
        const.DATE_NAME,
        const.AC_VOL_NAME,
        const.AC_CURRENT_NAME,
        const.AC_CURRENT_DENSITY_NAME,
        const.RELAY_NAME,
    ]
    merged_ac = merged_ac.reindex(columns=columns_names)

    merge_dc, is_empty = get_dc_data(udl2_data=udl2_data, area=area)
    # merge_dc

    return merge_ac_dc(merged_ac, merge_dc)
