# coding: utf-8
# author: svtter
# time:
"""
AC related value compute
"""

import typing as t

import pandas as pd

from . import ac_percent
from .const.ac import (
    AC_DENSITY_NAME,
    AC_VOL_NAME,
    DC_DENSITY_NAME,
    JUDGE_METRIC_NAME,
    NIGHT_NAME,
    POLAR_NAME,
    RESISTIVITY_NAME,
)
from .value import get_max_min_average, get_value, poweron


def get_night_value(data: pd.DataFrame) -> t.Any:
    """
    获取"夜间2点到4点极化电位平均值（V_CSE)"
    :param data:
    :return:
    """
    return get_value(data, NIGHT_NAME)


def get_resistivity(data: pd.DataFrame) -> t.Any:
    """
    获取土壤电阻率
    :param data:
    :return:
    """
    return get_value(data, RESISTIVITY_NAME)


def polar(
    data: pd.DataFrame,
    judge_metric: float,
    percent_func: t.Callable[[pd.Series, float], list] = ac_percent.polarization_point,
) -> list:
    """
    polarization potential
    极化电位
    """
    # data series

    res = get_max_min_average(POLAR_NAME, data)
    res = [*res, *percent_func(data[POLAR_NAME].dropna(), judge_metric)]
    return res


def dc_density(data: pd.DataFrame) -> list:
    res = get_max_min_average(DC_DENSITY_NAME, data)
    res = [*res, *ac_percent.dc_density(data[DC_DENSITY_NAME].dropna())]
    return res


def ac_voltage(data: pd.DataFrame) -> list:
    res = get_max_min_average(AC_VOL_NAME, data)
    res = [*res, *ac_percent.ac_voltage(data[AC_VOL_NAME].dropna())]
    return res


def ac_density(data: pd.DataFrame) -> list:
    assert isinstance(data, pd.DataFrame), "critical error. data type is not same."
    res = get_max_min_average(AC_DENSITY_NAME, data)
    res = [*res, *ac_percent.ac_density(data[AC_DENSITY_NAME].dropna())]
    return res


def get_all(
    data: pd.DataFrame,
    judge_metrics: float,
    values: dict,
    interval_jihua: bool,
) -> list:
    res = [
        (JUDGE_METRIC_NAME, judge_metrics),
        *poweron(data),
        *polar(data, judge_metric=judge_metrics),
        *dc_density(data),
        *ac_voltage(data),
        *ac_density(data),
    ]

    return res
