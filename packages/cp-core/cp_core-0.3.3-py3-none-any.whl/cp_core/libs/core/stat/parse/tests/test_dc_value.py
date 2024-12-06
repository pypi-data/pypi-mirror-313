# coding: utf-8
# author: svtter
# time:
""" """

import unittest

from cp_core.libs.core.stat.parse.dc_value import (
    _filter_data,
    poweron,
)

from .base import get_data_sheet


class ValueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = get_data_sheet()

    def test_filter_data(self):
        df = _filter_data(self.data, types="poweron")
        print(df)

    def test_tongdian(self):
        poweron(self.data)
        pass

    def test_get_all(self):
        # res = get_all(self.data, judge_metrics=-0.774)
        # print(res)
        pass
