# coding: utf-8

import os
import unittest

import pandas as pd

from cp_core.config import csv_folder, project_root
from cp_core.libs.core.checker import check_col
from cp_core.libs.core.filter.fileutils import open_anko_file, write_file
from cp_core.libs.core.filter.parse import const, date, merge
from cp_core.tests.path import test2, test3, udl2_path


class ProcessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(udl2_path, encoding="gbk")
        self.data2_path = os.path.join(
            project_root, csv_folder, "data/filter/udl2_DW06-20057.csv"
        )
        self.data_with_missing = pd.read_csv(self.data2_path, encoding="gbk")
        self.columns_names = [
            const.DATE_NAME,
            const.POWER_ON_NAME,
            const.POLAR_NAME,
            const.DC_CURRENT_NAME,
            const.DC_CURRENT_DENSITY_NAME,
            const.AC_CURRENT_NAME,
            const.AC_VOL_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            const.STATUS_NAME,
        ]

    def test_merge_anko(self):
        udl2_data = pd.read_csv(test3.get("udl2_path"), encoding="gbk")
        anko_data = open_anko_file(test3.get("anko_path"))

        merge_all = merge.get_merge_data_from_anko(udl2_data, anko_data, area=1.0)
        self.assertFalse(merge_all.empty)

    def test_merge_udl1(self):
        udl2_data = pd.read_csv(test2.get("udl2_path"), encoding="gbk")
        udl1_data = pd.read_csv(test2.get("udl1_path"), encoding="gbk")

        udl2_data, start = date.str2datetime_first_time(data=udl2_data)
        current_date = pd.to_datetime(start)

        merge_all = merge.get_merge_data_from_udl1(udl2_data, udl1_data, area=1.0)
        self.assertEqual(
            current_date, pd.to_datetime(merge_all.loc[0, const.DATE_NAME])
        )
        self.assertFalse(merge_all.empty)

    def test_merge_udl2(self):
        merge_all = merge.get_merge_data_from_udl2(self.data, area=1.0)
        self.assertFalse(merge_all.empty)

        merge_all = merge.get_merge_data_from_udl2(self.data_with_missing, area=1.0)
        self.assertFalse(merge_all.empty)

    def test_relay_name_in_merge_udl2(self):
        df = merge.get_merge_data_from_udl2(self.data, area=1.0)
        # df.to_csv("./tmp/look-merge-udl2.csv", index=False)
        check_col(df, const.STATUS_NAME)

    def test_merge_udl2_with_dirty(self):
        data = self.data_with_missing
        merge_all = merge.get_merge_data_from_udl2(data, area=1.0)
        self.assertFalse(merge_all.empty)
        self.assertListEqual(self.columns_names, list(merge_all.head()))

        timestamp = "5/8/2019  10:27:00 AM"
        current_date = pd.to_datetime(timestamp)
        # self.assertIsNone(merge_all[:, DATE_NAME == current_date][AC_CURRENT_NAME].iloc[0])

    def test_merge_ac_dc(self):
        # udl2
        data, start = date.str2datetime_first_time(self.data)

        merged_ac, is_empty = merge.get_ac_data(df=data, start=start, area=1.0)
        current_date = merged_ac.loc[0, const.DATE_NAME]
        assert not is_empty
        merged_dc, is_empty = merge.get_dc_data(udl2_data=data, area=1.0)
        assert not is_empty
        res = merge.merge_ac_dc(merged_ac, merged_dc)
        date2 = res.loc[0, const.DATE_NAME]
        self.assertFalse(res.empty)
        self.assertEqual(current_date, date2)

        data, start = date.str2datetime_first_time(self.data_with_missing)
        merged_ac, is_empty = merge.get_ac_data(df=data, start=start, area=1.0)
        assert is_empty
        merged_dc, is_empty = merge.get_dc_data(udl2_data=data, area=1.0)
        assert not is_empty
        res = merge.merge_ac_dc(merged_ac, merged_dc)
        check_col(res, const.STATUS_NAME)
        self.assertFalse(res.empty)
