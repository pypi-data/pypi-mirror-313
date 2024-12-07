# coding: utf-8
# author: svtter
# time:
""" """

from cp_core.libs.core.stat.parse.ac_value import (
    ac_density,
    ac_voltage,
    dc_density,
    get_resistivity,
    polar,
)


def test_get_value(get_data):
    data = get_data
    # data

    res = get_resistivity(data)
    assert res == 10.0
    # res


def test_jihua(get_data):
    data = get_data
    res = polar(data, judge_metric=-0.85)
    print(res)


def test_zhiliu(get_data):
    data = get_data
    res = dc_density(data)
    print(res)


def test_jiaoliu_dianya(get_data):
    data = get_data
    res = ac_voltage(data)
    print(res)


def test_jiaoliu_midu(get_data):
    data = get_data
    res = ac_density(data)
    print(res)


def test_get_all(get_data):
    data = get_data
    # res = get_all(data=data, judge_metrics=-0.85)
    # print(res)
    pass
