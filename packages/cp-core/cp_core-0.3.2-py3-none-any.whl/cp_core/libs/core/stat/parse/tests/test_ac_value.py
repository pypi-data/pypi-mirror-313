# coding: utf-8
# author: svtter
# time:
""" """

import unittest

from cp_core.libs.core.stat.parse.ac_value import (
    ac_density,
    ac_voltage,
    dc_density,
    get_resistivity,
    polar,
)

from .base import get_data


class ValueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = get_data()

    def test_get_value(self):
        data = self.data
        data = get_data()
        # data

        res = get_resistivity(data)
        self.assertEqual(res, 10.0)
        # res

    def test_jihua(self):
        data = self.data
        res = polar(data, judge_metric=-0.85)
        print(res)

    def test_zhiliu(self):
        res = dc_density(self.data)
        print(res)

    def test_jiaoliu_dianya(self):
        res = ac_voltage(self.data)
        print(res)

    def test_jiaoliu_midu(self):
        res = ac_density(self.data)
        print(res)

    def test_get_all(self):
        # res = get_all(data=self.data, judge_metrics=-0.85)
        # print(res)
        pass
