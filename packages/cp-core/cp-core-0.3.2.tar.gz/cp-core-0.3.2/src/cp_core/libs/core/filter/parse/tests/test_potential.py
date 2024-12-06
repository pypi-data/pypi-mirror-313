# coding: utf-8

import unittest

import pandas as pd

from cp_core.libs.core.filter.parse import const, date
from cp_core.libs.core.filter.parse.potential import (
    potential_ac_reading,
    potential_dc_reading,
)
from cp_core.libs.core.filter.parse.udl1_ac import ac_reading_from_udl1
from cp_core.tests.path import test2, udl2_path


class ProcessTest(unittest.TestCase):
    def test_potential_ac(self):
        data = pd.read_csv(udl2_path, encoding="gbk")

        # 获取需要的开始时间
        start = date.get_first_time(data)

        # 获取 Potential DC reading
        d = data.loc[data["Record Type"] == const.CP_AC_READING]
        d = date.str2datetime(d)
        d = date.locate_time(d, first_time=start)
        final_res = potential_ac_reading(d)
        # final_res

    def test_ac_reading(self):
        udl2_data = pd.read_csv(test2.get("udl2_path"), encoding="gbk")
        udl1_data = pd.read_csv(test2.get("udl1_path"), encoding="gbk")

        # 获取需要的开始时间
        start = date.get_first_time(udl2_data)
        data = ac_reading_from_udl1(udl1_data, start)
        # data

    def test_potential_dc(self):
        data = pd.read_csv(udl2_path, encoding="gbk")

        # 获取需要的开始时间
        start = date.get_first_time(data)

        # 获取 Potential DC reading
        d = data.loc[data["Record Type"] == const.CP_DC_READING]
        d = date.str2datetime(d)
        d = date.locate_time(d, first_time=start)
        final_res = potential_dc_reading(d)
