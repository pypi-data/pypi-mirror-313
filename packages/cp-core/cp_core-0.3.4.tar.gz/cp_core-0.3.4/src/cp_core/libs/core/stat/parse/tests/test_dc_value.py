# coding: utf-8
# author: svtter
# time:
""" """

from cp_core.libs.core.stat.parse.dc_value import (
    _filter_data,
    poweron,
)


def test_filter_data(get_data_sheet):
    data = get_data_sheet
    df = _filter_data(data, types="poweron")
    print(df)


def test_tongdian(get_data_sheet):
    data = get_data_sheet
    poweron(data)
    pass


def test_get_all(get_data_sheet):
    data = get_data_sheet
    # res = get_all(data, judge_metrics=-0.774)
    # print(res)
    pass
