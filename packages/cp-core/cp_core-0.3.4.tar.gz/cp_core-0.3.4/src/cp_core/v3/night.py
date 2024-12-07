import functools
import typing as t

import pandas as pd

from cp_core.libs.core.filter.parse import const, merge, statistic


def filter_dc(row_name: str) -> t.Callable:
    """通过行数据过滤"""

    def decarate(func: t.Callable) -> t.Callable:
        @functools.wraps(func)
        def wrapper(data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
            df = merge.filter_reading(data, row_name)
            return func(df, *args, **kwargs)

        return wrapper

    return decarate


def extract_night_data(
    data: pd.DataFrame,
    from_col=const.pDC,
    to_col=const.NIGHT_POWERON,
    df_filter: t.Callable[[pd.DataFrame], pd.DataFrame] = lambda x: x,
) -> pd.DataFrame:
    df = data[[const.DATE_NAME, from_col, const.RELAY_NAME]].copy()
    df = df_filter(df)
    if df.empty:
        return df

    df = df.apply(lambda x: statistic.filter_time(x, from_col), axis=1)
    df = df.dropna(axis=0, how="any")

    # 添加夜值
    df[to_col] = df[from_col]

    # 删除原极化值
    df = df.drop(columns=[from_col, const.RELAY_NAME])
    return df


@filter_dc(const.CP_DC_READING)
def extract_night_poweron_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    提取夜间通电电位数据
    """
    return extract_night_data(
        data,
        from_col=const.pDC,
        to_col=const.NIGHT_POWERON,
        df_filter=lambda df: filter_relay_name(df, 1),
    )


def filter_relay_name(data: pd.DataFrame, value: int) -> pd.DataFrame:
    return data[data[const.RELAY_NAME] == value]


@filter_dc(const.CP_DC_OFF_READING)
def extract_night_polar_avg(data: pd.DataFrame) -> pd.DataFrame:
    df = extract_night_data(
        data,
        from_col=const.pDC_off,
        to_col=const.NIGHT_POLAR_AVG,
        df_filter=lambda df: filter_relay_name(df, 0),
    )

    # 计算夜平均值
    avg_v = df[const.NIGHT_POLAR_AVG].mean()
    df[const.NIGHT_POLAR_AVG] = avg_v
    return df


def merge_night_data(
    poweron_data: pd.DataFrame, polar_avg: pd.DataFrame
) -> pd.DataFrame:
    return pd.merge(
        left=poweron_data,
        right=polar_avg,
        left_on=const.DATE_NAME,
        right_on=const.DATE_NAME,
        how="outer",
    )
