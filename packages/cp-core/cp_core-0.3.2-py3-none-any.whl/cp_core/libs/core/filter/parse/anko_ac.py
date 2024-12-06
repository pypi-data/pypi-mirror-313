"""
handle the anko file
"""

from .date import str2datetime, locate_time
from .const import AC_VOL_NAME, ANKO_DATE_NAME


AC_NAME = "Vac(V)"
DATE_NAME = ANKO_DATE_NAME


def ac_reading_from_anko(data, start):
    """
    Data should be udl1.

    """
    d = transfer_datetime(data)
    d = locate_time(d, first_time=start, date_name=DATE_NAME)

    # d: 已经进行时间过滤的数据
    dc_col = d[[DATE_NAME, AC_NAME]]
    dc_col.rename(columns={AC_NAME: AC_VOL_NAME}, inplace=True)

    return dc_col


def transfer_datetime(data):
    """
    将两列数据合并成一列，并且赋值
    data: transferred data
    """

    def gen_datetime(row):
        return row["Date"] + " " + row["Time"]

    data[DATE_NAME] = data.apply(gen_datetime, axis=1)
    data = str2datetime(data, date_name=DATE_NAME)
    return data
