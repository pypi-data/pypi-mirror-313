"""
Functions about ac-reading
"""

import pandas as pd

from ..errors import ColumnError
from . import const


def ac_update_init(df: pd.DataFrame, area: float) -> pd.DataFrame:
    """Update value according to unit.

    Parameters
    ----------
    df :
    area :

    Returns
    -------

    Raises
    ------

    ValueError:

    """
    df = df[[const.DATE_NAME, const.cAC, const.RELAY_NAME, const.cAC_UNIT]]
    # check_df_numbers(dc_col)
    unit = df[const.cAC_UNIT].iloc[0]
    ac_reading = df[const.cAC]

    if unit == "A":
        density = ac_reading / area * 10000
        ac_reading = ac_reading * 1000
    elif unit == "A/m2":
        density = ac_reading.copy()
        ac_reading = ac_reading * (area / 10000) * 1000
    else:
        raise ColumnError("ac unit error.")

    df.update(ac_reading)
    df.insert(0, const.AC_CURRENT_NAME, ac_reading)
    df.insert(0, const.AC_CURRENT_DENSITY_NAME, density)
    return df.reindex(
        columns=[
            const.DATE_NAME,
            const.cAC,
            const.AC_CURRENT_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            const.RELAY_NAME,
        ]
    )


def current_ac_reading(df: pd.DataFrame, area: float) -> pd.DataFrame:
    """get ac reading from data.

    Parameters
    ----------
    df : filtered data
    area :  piece area

    Returns
    -------
    current ac reading data frame.

    """
    ac_col = ac_update_init(df, area)

    # dc_col = filter_ac(dc_col, area)
    # set the relay enable number is 0 to None
    ac_col.loc[ac_col[const.RELAY_NAME] == 0, const.AC_CURRENT_NAME] = None
    ac_col.loc[ac_col[const.RELAY_NAME] == 0, const.AC_CURRENT_DENSITY_NAME] = None
    return ac_col


def dc_update_init(df: pd.DataFrame, area: float) -> pd.DataFrame:
    """
    更新初始化参数

    :param df:
    :param area:
    :return:
    """

    unit = df[const.cDC_UNIT].iloc[0]
    dc_reading = df[const.cDC]

    if unit == "A":
        density = dc_reading / area * 10000
        dc_reading = dc_reading * 1000
    elif unit == "A/m2":
        density = dc_reading.copy()
        dc_reading = dc_reading * (area / 10000) * 1000
    else:
        raise ColumnError("ac unit error.")

    df.update(dc_reading)
    df.insert(0, const.DC_CURRENT_NAME, dc_reading)
    df.insert(0, const.DC_CURRENT_DENSITY_NAME, density)
    columns_names = [
        const.DATE_NAME,
        const.cDC,
        const.DC_CURRENT_NAME,
        const.DC_CURRENT_DENSITY_NAME,
        const.RELAY_NAME,
    ]
    return df.reindex(columns=columns_names)


def current_dc_reading(d: pd.DataFrame, area: float) -> pd.DataFrame:
    """
    获取 current dc reading 数据
    d: 已经进行时间过滤的数据
    area: 面积
    """

    # dc_col = cp_to_handle(d)
    # 提取部分数据
    dc_col = d[[const.DATE_NAME, const.cDC, const.RELAY_NAME, const.cDC_UNIT]]

    dc_col = dc_update_init(dc_col, area)

    # dc_col = filter_dc(dc_col, area)
    dc_col.loc[dc_col[const.RELAY_NAME] == 0, const.DC_CURRENT_NAME] = None
    dc_col.loc[dc_col[const.RELAY_NAME] == 0, const.DC_CURRENT_DENSITY_NAME] = None

    return dc_col
