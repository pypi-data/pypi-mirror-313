# coding: utf-8

import os
import unittest

import pandas as pd

from cp_core.config import csv_folder, project_root
from cp_core.libs.core.filter.check import check_col
from cp_core.libs.core.filter.parse import const, current_reading, date, merge
from cp_core.tests.path import test2, test3, udl2_path


class MergeACTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(udl2_path, encoding="gbk")
        self.data2_path = os.path.join(
            project_root, csv_folder, "data/filter/udl2_DW06-20057.csv"
        )
        self.data_with_missing = pd.read_csv(self.data2_path, encoding="gbk")

    def test_current_ac(self):
        data = pd.read_csv(udl2_path, encoding="gbk")

        # 获取开始的时间
        data = date.str2datetime(data)
        start = date.get_first_time(data)

        # 获取 Current AC reading
        d = data.loc[data["Record Type"] == const.CC_AC_READING]
        d = date.locate_time(d, first_time=start)
        d = current_reading.current_ac_reading(d, area=1.0)
        self.assertLess(1, len(d.index))

        # d[[DATE_NAME, cAC_NAME]]

    def test_get_current_ac_reading(self):
        data = self.data
        data = date.str2datetime(data)
        start = date.get_first_time(data)
        res = merge.filter_current_ac_reading(data, start, area=1.0)

        self.assertFalse(res.empty)
        self.assertIsNotNone(res)

        # test data missing.
        data = self.data_with_missing
        data = date.str2datetime(data)
        start = date.get_first_time(data)
        res = merge.filter_current_ac_reading(data, start, area=1.0)

        columns_names = [
            const.DATE_NAME,
            const.cAC,
            const.AC_CURRENT_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            const.RELAY_NAME,
        ]
        self.assertListEqual(columns_names, list(res))
        self.assertTrue(res.empty)
        self.assertIsNotNone(res)

    def test_get_potential_ac_reading(self):
        data = pd.read_csv(udl2_path, encoding="gbk")

        data, start = date.str2datetime_first_time(data)
        potential_ac_df = merge.filter_potential_ac_reading(data, start)

        self.assertIsNotNone(potential_ac_df)
        self.assertLess(1, len(potential_ac_df.index))

    def test_relay_name_in_pAC(self):
        data, start = date.str2datetime_first_time(self.data)
        df = merge.filter_potential_ac_reading(data, start)
        check_col(df, const.RELAY_NAME)

    def test_relay_name_in_cAC(self):
        data, start = date.str2datetime_first_time(self.data)
        df = merge.filter_current_ac_reading(data, start, area=1.0)
        check_col(df, const.RELAY_NAME)

    def test_relay_name_in_ac_data(self):
        data, start = date.str2datetime_first_time(self.data)
        res, is_empty = merge.get_ac_data(data, start=start, area=1.0)
        check_col(res, const.RELAY_NAME)

    def test_get_ac_data(self):
        # write test first
        data, start = date.str2datetime_first_time(self.data)
        res, is_empty = merge.get_ac_data(data, start=start, area=1.0)
        assert res.empty == is_empty

        data, start = date.str2datetime_first_time(self.data_with_missing)
        res, is_empty = merge.get_ac_data(data, start=start, area=1.0)
        assert res.empty == is_empty
