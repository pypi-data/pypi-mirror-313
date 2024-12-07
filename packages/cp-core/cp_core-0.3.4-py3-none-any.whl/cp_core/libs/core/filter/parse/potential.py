"""
Functions about dc-reading
TODO: change the name of function and CONST
"""

import pandas as pd

from . import const


def potential_ac_reading(d: pd.DataFrame) -> pd.DataFrame:
    """
    d: 已经进行时间过滤的数据
    """

    # 整理 AC 的数据
    df = d[[const.DATE_NAME, const.pAC, const.RELAY_NAME]]
    df.insert(2, const.AC_VOL_NAME, df[const.pAC])

    # dc_col = filter_ac(dc_col)
    df.loc[df[const.RELAY_NAME] == 0, const.AC_VOL_NAME] = None
    column_names = [
        const.DATE_NAME,
        const.pAC,
        const.AC_VOL_NAME,
        const.RELAY_NAME,
    ]
    df = df.reindex(columns=column_names, fill_value="test")
    return df


def potential_dc_reading(d: pd.DataFrame) -> pd.DataFrame:
    """
    d: 从第5s开始，已经进行时间过滤的数据；
    """
    # dc_col = cp_to_handle(d)
    # 整理数据，将数据排列进去
    dc_col = d[[const.DATE_NAME, const.pDC, const.RELAY_NAME]]
    dc_col.insert(0, const.POWER_ON_NAME, dc_col[const.pDC])
    dc_col.insert(0, const.POLAR_NAME, dc_col[const.pDC])

    # sort the head.
    columns_names = [
        const.DATE_NAME,
        const.pDC,
        const.POWER_ON_NAME,
        const.POLAR_NAME,
        const.RELAY_NAME,
    ]
    dc_col = dc_col.reindex(columns=columns_names)

    # dc_col = filter_dc(dc_col)
    # 根据 relay name，去除部分数据
    dc_col.loc[dc_col[const.RELAY_NAME] == 0, const.POWER_ON_NAME] = None
    dc_col.loc[dc_col[const.RELAY_NAME] == 1, const.POLAR_NAME] = None
    return dc_col
