"""
时间相关的数据处理
Data process about time
"""

from datetime import timedelta
from typing import Tuple

import pandas as pd

from cp_core.config import logger

from . import const


def get_first_time(data: pd.DataFrame) -> str:
    """
    get the first time
    data: origin data
    :rtype:
    """
    d = data.loc[data["Record Type"] == const.CP_DC_READING]
    # d = d.loc[data['Relay Enabled'] == 1]
    t = d[const.DATE_NAME].iloc[0]
    # start = add_time(t)
    t = pd.to_datetime(t)
    start = t + timedelta(seconds=5)
    return start.strftime("%m-%d-%Y %H:%M:%S")


def locate_time(d, first_time: str, date_name=const.DATE_NAME) -> pd.DataFrame:
    """
    remove previous needless data
    d: filtered data
    first_time: first time
    date_name: .
    """
    res = d.loc[d[date_name] >= pd.to_datetime(first_time)]
    return res


def str2datetime(d: pd.DataFrame, date_name=const.DATE_NAME) -> pd.DataFrame:
    """
    transfer the time data in origin data to python-format datetime data
    """
    d[date_name] = pd.to_datetime(d[date_name])
    # d[date_name] = pd.to_datetime(d[date_name], format='%m/%d/%Y %H:%M:%S')
    # d[date_name] = pd.to_datetime(d[date_name], format='%m-%d-%Y %H:%M:%S')
    logger.info("transfer time to datetime")
    return d


def str2datetime_first_time(
    data: pd.DataFrame, date_name=const.DATE_NAME
) -> Tuple[pd.DataFrame, str]:
    """
    combine two functions
    """

    # 时间转换
    data = str2datetime(data)
    start = get_first_time(data)

    return data, start
