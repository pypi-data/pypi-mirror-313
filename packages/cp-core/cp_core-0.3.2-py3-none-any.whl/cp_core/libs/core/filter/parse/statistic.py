"""
最后再进一次运算

Not confirm
"""

import math
import os
import sys
import typing
from datetime import datetime, timedelta
from functools import partial
from typing import Tuple

import numpy as np
import pandas as pd

from cp_core.config import DEBUG
from cp_core.libs.core.filter.errors import EmptyError

from . import const


def filter_time(data: pd.Series, column_name: str = const.POLAR_NAME):
    """
    filter 2am - 3:30am data
    """
    # print(data)
    date = data[const.DATE_NAME].to_pydatetime()

    if (date.hour == 2) or (date.hour == 3 and 0 <= date.minute <= 30):
        return data
    else:
        data[column_name] = None
        return data


def filter_near(data: pd.Series, prev, delta, keepData: bool = False):
    """remove nearby data by value, just get the first appears data.
    时间提取算法
    Parameters
    ----------
    data : current data
    prev : previous time
    delta : time delta

    Returns
    -------

    """
    # 当前时间
    current = data[const.DATE_NAME].to_pydatetime()

    if keepData and math.isnan(data[const.POLAR_NAME]):
        return data

    # debug_filter_near(data)
    # 判断当前数据是否是下一秒的数据
    if prev.get("value") + delta == current:
        prev["value"] = current
        return None
    else:
        prev["value"] = current
        return data


def debug_filter_near(data):
    if DEBUG:
        # 调试迭代数据
        from tests.media import MEDIA_FOLDER

        with open(os.path.join(MEDIA_FOLDER, "temp.txt"), "a") as f:
            f.write(
                f"id: {data.name}, {data[const.POLAR_NAME]}, type: {type(data[const.POLAR_NAME])}\n"
            )


def get_date(data: pd.DataFrame) -> typing.List[datetime]:
    """get date list. if two days in data, return [date, date]
    Parameters
    ----------
    data :

    Returns
    -------

    """
    res = data[const.DATE_NAME]
    first_data = res.iloc[0]
    assert isinstance(first_data, datetime), first_data
    assert isinstance(res, pd.Series), res

    date = first_data.date()
    for d in res:
        if d.date() != date:
            return [first_data, d]
    return [first_data]


def get_night_value(origin_data: pd.DataFrame) -> float:
    """
    获取夜间数据的平均值

    主要功能：
    1. 提取凌晨2点到3点30分之间的数据
    2. 确保数据的时间连续性
    3. 处理跨天的情况
    4. 计算该时段数据的平均值

    Parameters:
        origin_data: 包含时间和计划值的DataFrame
    Returns:
        float: 夜间数据的平均值
    """
    # 步骤1: 数据预处理
    # 只保留日期时间和极化值两列
    data = origin_data[[const.DATE_NAME, const.POLAR_NAME]].copy()
    if data.empty:
        raise EmptyError("The night value error is empty.")

    # 删除包含任何空值的行
    data = data.dropna(axis=0, how="any")

    # 步骤2: 时间连续性过滤
    # 初始化时间比较器和时间间隔(1秒)
    prev = {"value": datetime.now()}
    delta = timedelta(seconds=1)
    # 使用偏函数创建过滤器，去除时间连续的重复数据点
    f_near = partial(filter_near, prev=prev, delta=delta)
    data = data.apply(f_near, axis=1)
    data = data.dropna(axis=0, how="any")

    # 步骤3: 时间段过滤
    # 只保留凌晨2点到3点30分之间的数据
    data = data.apply(filter_time, axis=1)
    data = data.dropna(axis=0, how="any")
    if data.empty:
        raise EmptyError("The night value error is empty.")

    # 步骤4: 跨天处理
    # 如果数据包含多天，只取第一天的数据
    date_list = get_date(data)
    if len(date_list) > 1:
        data = data[data[const.DATE_NAME] > date_list[0]]

    # 步骤5: 计算并返回结果
    # 计算过滤后的计划值的平均值
    res = data.mean()[const.POLAR_NAME]
    return res
