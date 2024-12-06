# coding: utf-8
# author: svtter
# time: ...

""" """

from .const.dc import (
    DENSITY_PERCENT_VALUE,
    DENSITY_VALUE,
    POLAR_VALUE_WITH_PROTECT,
    POLAR_VALUE_WITHOUT_PROTECT,
)
from .percent import OPMetric, Variable, get_count, stat_func


def polarization(se, metric, is_protect) -> list:
    """
    极化电位
    """
    name = POLAR_VALUE_WITH_PROTECT if is_protect else POLAR_VALUE_WITHOUT_PROTECT
    if is_protect:
        percent = [
            get_count(se, se > metric),
            get_count(se, se > metric + 0.05),
            get_count(se, se > metric + 0.1),
            get_count(se, se > metric + 0.85),
            get_count(se, se < metric - 0.1),
            get_count(se, se < metric - 0.2),
            get_count(se, se < metric - 0.35),
        ]
    else:
        percent = [
            get_count(se, se > metric),
            get_count(se, se > metric + 0.02),
            get_count(se, se > metric + 0.1),
            get_count(se, se < metric - 0.02),
            get_count(se, se < metric - 0.100),
        ]

    res = [(name, val) for name, val in zip(name, percent)]
    return res


def density_v2(se):
    op_metric = [
        OPMetric(op=">", metric=1),
        OPMetric(op=">", metric=0.1),
        OPMetric(op=">", metric=0),
        OPMetric(op="<", metric=0),
        OPMetric(op="<", metric=-0.1),
        OPMetric(op="<", metric=-1),
    ]
    var = Variable(name="直流电流密度", unit="A/m^2")
    res = stat_func(se, var, op_metric)
    return res


def density(se) -> list:
    percent = [
        get_count(se, se > 1),
        get_count(se, se > 0.1),
        get_count(se, se > 0),
        get_count(se, se < 0),
        get_count(se, se < -0.1),
        get_count(se, se < -1),
    ]
    res = [(name, val) for name, val in zip(DENSITY_PERCENT_VALUE, percent)]
    return res


def filter_density(data):
    value = [
        data[data > 1].mean(),
        data[data > 0.1].mean(),
        data[data > 0].mean(),
        data[data < 0].mean(),
        data[data < -0.1].mean(),
        data[data < -1].mean(),
    ]
    res = [(name, val) for name, val in zip(DENSITY_VALUE, value)]
    return res
