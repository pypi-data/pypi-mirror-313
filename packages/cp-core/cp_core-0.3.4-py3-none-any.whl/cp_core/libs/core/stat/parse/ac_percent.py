# coding: utf-8

from .const import ac as const_ac
from .percent import get_count


def polarization_point(
    se,
    metric: float,
    POLAR_VALUE=const_ac.POLAR_VALUE,
    value_list: list[tuple[str, float]] = [
        (">", 0),
        (">", 0.05),
        (">", 0.1),
        (">", 0.85),
        ("<", -0.1),
        ("<", -0.2),
        ("<", -0.35),
    ],
):
    """
    极化电位
    polarization point
    :param se:
    :param metric:
    :return:
    """

    def compare(se, value):
        if value[0] == ">":
            return se > metric + value[1]
        return se < metric + value[1]

    percent = [get_count(se, compare(se, value)) for value in value_list]
    res = [(name, val) for name, val in zip(POLAR_VALUE, percent)]
    return res


def dc_density(se):
    """
    直流电流密度
    :param se:
    :return:
    """
    percent = [
        get_count(se, se > 1),
        get_count(se, se > 0.1),
        get_count(se, se > 0),
        get_count(se, se < 0),
        get_count(se, se < -0.1),
        get_count(se, se < -1),
    ]

    res = [(name, val) for name, val in zip(const_ac.DC_DENSITY_VALUE, percent)]
    return res


def ac_voltage(se):
    """交流电压
    :param se:
    :return:
    """
    percent = [
        get_count(se, se >= 15),
        get_count(se, se > 10),
        get_count(se, se > 4),
    ]

    res = [(name, val) for name, val in zip(const_ac.AC_VOL_VALUE, percent)]
    return res


def ac_density(se):
    """
    交流电压密度

    :param se:
    :return:
    """

    percent = [
        get_count(se, se > 300),
        get_count(se, se >= 100),
        get_count(se, se.between(30, 100, inclusive="both")),
        get_count(se, se < 30),
    ]

    res = [(name, val) for name, val in zip(const_ac.AC_DENSITY_VALUE, percent)]
    return res
