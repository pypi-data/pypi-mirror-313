"""
处理udl1 ac reading
"""
import pandas as pd
from .date import str2datetime, locate_time
from .const import AC_VOL_NAME, UDL1_DATE_NAME


AC_NAME = "AC Reading"
DATE_NAME = UDL1_DATE_NAME


def _filter_ac_reading(d: pd.DataFrame) -> pd.DataFrame:
    """
    d: 已经进行时间过滤的数据
    """

    dc_col = d[[DATE_NAME, AC_NAME]]
    dc_col.rename(columns={AC_NAME: AC_VOL_NAME}, inplace=True)
    return dc_col


def ac_reading_from_udl1(data: pd.DataFrame, start: str) -> pd.DataFrame:
    """
    Data should be udl1.

    """
    d = data.loc[data["Record Type"] == AC_NAME]
    d = str2datetime(d, date_name=DATE_NAME)
    d = locate_time(d, first_time=start, date_name=DATE_NAME)
    final_res = _filter_ac_reading(d)
    return final_res
