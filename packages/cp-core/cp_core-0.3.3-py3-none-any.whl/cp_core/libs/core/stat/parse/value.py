# coding: utf-8
# author: svtter
# time: ...

"""
直流交流共用函数
"""

import typing as t

import pandas as pd

from .const.ac import POWER_ON_NAME


def get_value(data: pd.DataFrame, name: str) -> t.Any:
    """
    get the value of according to value name.
    """
    my_data = data.copy()
    return my_data[name][0]


def get_max_min_average(name: str, data: pd.DataFrame) -> list:
    """
    get the max min average value of $name
    :param name:
    :param data:
    :return:
    """
    se = data[name]
    se.dropna(inplace=True)
    res = [
        (name + "_max", se.max()),
        (name + "_min", se.min()),
        (name + "_average", se.mean()),
    ]
    return res


def poweron(data: pd.DataFrame) -> list:
    # data series
    res = get_max_min_average(POWER_ON_NAME, data)
    return res
