import datetime
import functools
import typing as t

import pandas as pd

from cp_core.libs.core.filter import extract, forms
from cp_core.libs.core.filter.errors import EmptyError
from cp_core.libs.core.filter.parse import date, merge, night
from cp_core.libs.core.filter.parse import statistic as stat

from . import const, func


def extract_data_from_udl2(
    data,
    params: forms.InputData,
) -> pd.DataFrame:
    """udl2 数据提取函数, v2"""
    data = get_merge_data_from_udl2(data, params.piece_area)

    add_column_data = extract.use_add_column(params)
    data = add_column_data(data)
    return data


def get_merge_data_from_udl2(
    df: pd.DataFrame,
    area: float,
) -> pd.DataFrame:
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

    merged_ac = get_ac_data(df=df, start=start, area=area)
    merged_dc = get_dc_data(udl2_data=df, area=area)

    columns_names = [
        const.filter.DATE_NAME,
        const.filter.POWER_ON_NAME,
        const.NIGHT_POWERON,
        const.filter.POLAR_NAME,
        const.NIGHT_POLAR,
        const.filter.DC_CURRENT_NAME,
        const.filter.DC_CURRENT_DENSITY_NAME,
        const.filter.AC_CURRENT_NAME,
        const.filter.AC_VOL_NAME,
        const.filter.AC_CURRENT_DENSITY_NAME,
        const.filter.STATUS_NAME,
    ]
    merged_all = merge.merge_ac_dc(merged_ac, merged_dc)
    return merged_all.reindex(columns=columns_names)


@func.empty_checker(name="ac_data")
def get_ac_data(
    df: pd.DataFrame,
    start: str,
    area: float,
) -> pd.DataFrame:
    """get ac data from udl2.

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
    current_ac_df = merge.filter_current_ac_reading(df, start, area)
    potential_ac_df = merge.filter_potential_ac_reading(df, start)

    # remove abundant elements
    potential_ac_df = potential_ac_df.drop(const.filter.pAC, axis=1)
    potential_ac_df = potential_ac_df.drop(const.filter.RELAY_NAME, axis=1)
    current_ac_df = current_ac_df.drop(const.filter.cAC, axis=1)
    # c_ac_df = c_ac_df.drop(RELAY_NAME, axis=1)

    merged_ac = pd.merge(
        left=potential_ac_df,
        right=current_ac_df,
        left_on=const.filter.DATE_NAME,
        right_on=const.filter.DATE_NAME,
    )

    return merged_ac


@func.empty_checker(name="dc_data")
def get_dc_data(udl2_data: pd.DataFrame, area: float) -> pd.DataFrame:
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
    current_dc_df = merge.get_current_dc_reading(udl2_data, start, area)
    potential_dc_df = merge.get_potential_dc_reading(udl2_data, start)
    night_polar_df = night_polar(udl2_data, start)
    night_poweron_df = night_poweron(udl2_data, start)

    # potential_dc_df.to_csv("potential_dc_df.csv")
    current_dc_df = current_dc_df.drop(const.filter.cDC, axis=1)
    potential_dc_df = potential_dc_df.drop(const.filter.pDC, axis=1)
    potential_dc_df = potential_dc_df.drop(const.filter.RELAY_NAME, axis=1)

    def my_merge(df1, df2):
        return pd.merge(
            df1,
            df2,
            left_on=const.filter.DATE_NAME,
            right_on=const.filter.DATE_NAME,
            how="outer",
        )

    merge_dc = functools.reduce(
        my_merge, [current_dc_df, potential_dc_df, night_polar_df, night_poweron_df]
    )

    # merge_dc
    return merge_dc


def filter_fn(
    d: pd.DataFrame,
    from_col: str,
    to_col: str,
):
    """
    old_df col -> df col
    如果异常，处理之后返回的数据只有时间列和空列
    from_col: 数据来源列
    to_col: 新数据列
    """
    try:
        df = d[[const.filter.DATE_NAME, from_col]]
        df = get_night_value(df, ori_col=from_col)
        df = df.rename(columns={from_col: to_col})
    except EmptyError:
        # 如果数据为空，保留 date，返回空值
        df = d[[const.filter.DATE_NAME, to_col]]
        df[to_col] = None
    return df


def night_polar(data: pd.DataFrame, start: str) -> pd.DataFrame:
    return merge.filter_data(
        data,
        start,
        const.filter.CP_DC_OFF_READING,
        lambda d: filter_fn(d, from_col=const.filter.pDC_off, to_col=const.NIGHT_POLAR),
    )


def night_poweron(data: pd.DataFrame, start: str) -> pd.DataFrame:
    return merge.filter_data(
        data,
        start,
        const.filter.CP_DC_READING,
        lambda d: filter_fn(d, from_col=const.filter.pDC, to_col=const.NIGHT_POWERON),
    )


def get_night_value(
    origin_data,
    ori_col=const.filter.pDC,  # or pDC_off
) -> pd.DataFrame:
    """
    ori_col 从原始数据中提取的数据列名
    """
    data = origin_data[[const.filter.DATE_NAME, ori_col]]
    if data.empty:
        raise night.EmptyError("data missing.")

    # 删除包含任何空值的行
    data = data.dropna(axis=0, how="any")
    if data.empty:
        raise night.EmptyError("data missing.")

    # 步骤3: 时间段过滤
    # 只保留凌晨2点到3点30分之间的数据
    data = data.apply(lambda df: stat.filter_time(df, ori_col), axis=1)
    data = data.dropna(axis=0, how="any")
    return data
