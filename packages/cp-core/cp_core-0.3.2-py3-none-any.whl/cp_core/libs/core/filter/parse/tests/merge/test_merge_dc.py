# coding: utf-8

import os
import unittest

import pandas as pd

from cp_core.config import csv_folder, project_root
from cp_core.libs.core.checker import check_col
from cp_core.libs.core.filter.parse import const, date, merge
from cp_core.tests.path import test2, test3, udl2_path


class MergeDCTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(udl2_path, encoding="gbk")
        self.data2_path = os.path.join(
            project_root, csv_folder, "data/filter/udl2_DW06-20057.csv"
        )
        self.data_with_missing = pd.read_csv(self.data2_path, encoding="gbk")

    def test_get_dc_data(self):
        self.data = date.str2datetime(self.data)
        merged_dc, is_empty = merge.get_dc_data(udl2_data=self.data, area=100.0)
        assert merged_dc.empty == is_empty

        data = date.str2datetime(self.data_with_missing)
        merged_dc, is_empty = merge.get_dc_data(udl2_data=data, area=100.0)
        assert merged_dc.empty == is_empty

    def test_relay_name_in_dc_data(self):
        df, start = date.str2datetime_first_time(self.data)
        df, is_empty = merge.get_dc_data(udl2_data=df, area=100.0)
        assert not is_empty

        # df.to_csv("./tmp/look-dc-data.csv", index=False)
        check_col(df, const.RELAY_NAME)

    def test_get_current_dc_reading(self):
        self.data = date.str2datetime(self.data)
        start = date.get_first_time(self.data)
        res = merge.get_current_dc_reading(data=self.data, start=start, area=100.0)
        self.assertFalse(res.empty)
