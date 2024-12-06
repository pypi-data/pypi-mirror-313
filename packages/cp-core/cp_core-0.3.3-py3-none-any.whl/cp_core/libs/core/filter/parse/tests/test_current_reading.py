# coding: utf-8

import os
import unittest
from datetime import datetime

import pandas as pd

from cp_core.config import csv_folder, project_root
from cp_core.libs.core.checker import check_df_numbers
from cp_core.libs.core.filter.errors import EmptyError
from cp_core.libs.core.filter.parse import const
from cp_core.libs.core.filter.parse.current_reading import (
    ac_update_init,
    current_ac_reading,
    current_dc_reading,
)
from cp_core.libs.core.filter.parse.date import (
    get_first_time,
    locate_time,
    str2datetime,
    str2datetime_first_time,
)
from cp_core.libs.core.filter.parse.merge import (
    filter_current_ac_reading,
    filter_reading,
    get_ac_data,
    get_dc_data,
)
from cp_core.tests.path import udl2_path


class ProcessTest(unittest.TestCase):
    def setUp(self) -> None:
        data_path = (
            udl2_path,
            os.path.join(project_root, csv_folder, "data/filter/udl2_DW06-20057.csv"),
        )

        self.data = pd.read_csv(udl2_path, encoding="gbk")
        self.data_list = (pd.read_csv(path, encoding="gbk") for path in data_path)

    def test_update_unit_example(self):
        test_df = pd.DataFrame(
            {
                const.DATE_NAME: [datetime.now(), datetime.now()],
                const.cAC: [12.3, 12.4],
                const.RELAY_NAME: [1, 1],
                const.cAC_UNIT: ["A", "A"],
            }
        )
        df = ac_update_init(test_df, area=1.0)
        self.assertNotIn(const.cAC_UNIT, df.index)
        self.assertEqual(
            df[const.cAC].iloc[0],
            test_df[const.cAC].iloc[0] * 1000,
            msg=test_df[const.cAC].iloc[0],
        )

    def test_update_unit(self):
        for data in self.data_list:
            check_df_numbers(data)
            df = str2datetime(data)
            start = get_first_time(df)

            try:
                df = filter_reading(data, const.CC_AC_READING)
            except EmptyError as e:
                continue
            df = locate_time(df, first_time=start)
            df = ac_update_init(df, area=1.0)

            self.assertNotIn(const.cAC_UNIT, df.index)

    def test_get_ac_data(self):
        data, start = str2datetime_first_time(self.data)
        merged_ac, is_empty = get_ac_data(df=data, start=start, area=1.0)
        assert merged_ac.empty == is_empty

        for data in self.data_list:
            df, start = str2datetime_first_time(data)
            merged_ac, is_empty = get_ac_data(df=df, start=start, area=1.0)
            assert merged_ac.empty == is_empty

    def test_filter_ac_reading(self):
        data, start = str2datetime_first_time(self.data)
        current_ac_df = filter_current_ac_reading(data=data, start=start, area=1.0)
        self.assertFalse(current_ac_df.empty)

    def test_current_ac(self):
        # 获取开始的时间
        for data in self.data_list:
            d, start = str2datetime_first_time(data)

            # Get Coupon Current AC reading, coupon ac reading is a group
            try:
                d = filter_reading(data, const.CC_AC_READING)
            except EmptyError as e:
                # not test empty conditions
                continue

            d = locate_time(d, first_time=start)
            d = current_ac_reading(d, area=1.0)

            final_list = [
                const.DATE_NAME,
                const.cAC,
                const.AC_CURRENT_NAME,
                const.AC_CURRENT_DENSITY_NAME,
                const.RELAY_NAME,
            ]
            for item in final_list:
                self.assertIn(item, d.columns)

    def test_current_dc(self):
        data = pd.read_csv(udl2_path, encoding="gbk")

        # 获取开始的时间
        start = get_first_time(data)

        # 获取 Current DC reading
        d = data.loc[data["Record Type"] == const.CC_DC_READING]
        d = str2datetime(d)
        d = locate_time(d, first_time=start)
        d = current_dc_reading(d, area=1.0)

        self.assertLess(1, len(d.index))

    def test_relay_in_ac_data(self):
        data, start = str2datetime_first_time(self.data)
        merged_ac, is_empty = get_ac_data(df=data, start=start, area=1.0)
        assert const.RELAY_NAME in merged_ac.columns

    def test_status_in_dc_data(self):
        data, _ = str2datetime_first_time(self.data)
        merged_dc, is_empty = get_dc_data(udl2_data=data, area=1.0)
        assert const.RELAY_NAME in merged_dc.columns
