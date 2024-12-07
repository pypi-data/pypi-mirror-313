# coding: utf-8
# author: svtter
# time:
""" """

import unittest
from datetime import datetime, timedelta
from functools import partial

import numpy as np
import pandas as pd

from cp_core.libs.core.filter.errors import EmptyError
from cp_core.libs.core.filter.parse import const
from cp_core.libs.core.filter.parse.merge import (
    get_merge_data_from_udl2,
)
from cp_core.libs.core.filter.parse.statistic import (
    filter_near,
    filter_time,
    get_date,
    get_night_value,
)
from cp_core.tests.path import udl2_path


class NewTest(unittest.TestCase):
    def setUp(self):
        super(NewTest, self).setUp()
        data = pd.read_csv(udl2_path, encoding="gbk")
        self.area = 1.0
        self.data = get_merge_data_from_udl2(df=data, area=1.0)
        self.data_column = self.data[[const.DATE_NAME, const.POLAR_NAME]]

    def not_none(self, data: pd.DataFrame):
        self.assertLess(1, len(data.index))

    def test_filter_near_with_real(self):
        """使用真实数据看是否过滤成功"""
        mydate = datetime(year=2022, month=10, day=10, hour=2, minute=10, second=0)
        delta = timedelta(seconds=1)
        data = {
            const.DATE_NAME: [mydate, mydate + delta, mydate + delta * 2],
            "data": ["a", "b", "c"],
            const.POLAR_NAME: [1, 1, 1],
        }

        prev = {"value": datetime.now()}
        delta = timedelta(seconds=1)

        f_near = partial(filter_near, prev=prev, delta=delta)
        data = pd.DataFrame(data)
        data = data.apply(f_near, axis=1)
        data = data.dropna(axis=0, how="any")
        self.assertEqual(len(data), 1)

    def test_filter_near(self):
        data = self.data_column.dropna(axis=0, how="any")
        prev = {"value": datetime.now()}
        delta = timedelta(seconds=1)

        f_near = partial(filter_near, prev=prev, delta=delta)
        data = data.apply(f_near, axis=1)
        data = data.dropna(axis=0, how="any")
        self.not_none(data)

    def test_filter_data_with3pm(self):
        """new test"""
        mydate = datetime(year=2022, month=10, day=10, hour=2, minute=10, second=0)
        delta = timedelta(hours=2)
        data = {
            const.DATE_NAME: [mydate, mydate + delta, mydate + delta * 2],
            "data": ["a", "b", "c"],
            const.POLAR_NAME: [1, 1, 1],
        }
        df = pd.DataFrame(data)
        new_df = df.apply(filter_time, axis=1).dropna(axis=0, how="any")
        self.assertEqual(len(new_df), 1)
        # self.fail(new_df)

    @unittest.skip(reason="no suitable data.")
    def test_filter_time(self):
        data = self.data_column.dropna(axis=0, how="any")

        data = data.apply(filter_time, axis=1)
        data = data.dropna(axis=0, how="any")
        assert not data.empty

        res = data.mean()[const.POLAR_NAME]
        self.assertIsInstance(res, np.float64)

    def test_filter_data(self):
        """
        1. 直接过滤NAN数据
        2. filter neaby data
        3. filter 2am - 3:30am data.

        """
        mydate = datetime(year=2022, month=10, day=10, hour=2, minute=10, second=0)
        delta = timedelta(hours=2)
        data = pd.DataFrame(
            {
                const.DATE_NAME: [
                    mydate,
                    mydate + delta,
                    mydate + 2 * delta,
                    mydate + 3 * delta,
                ],
                const.POLAR_NAME: [1, 2, 3, 4],
            }
        )
        res = get_night_value(data)
        self.assertIsInstance(res, float)

        mydate = datetime(year=2022, month=10, day=10, hour=1, minute=10, second=0)
        data = pd.DataFrame(
            {const.DATE_NAME: [mydate, mydate + 2 * delta], const.POLAR_NAME: [1, 2]}
        )
        with self.assertRaises(EmptyError, msg=data):
            get_night_value(data)

    def test_get_date(self):
        data = pd.DataFrame(
            {
                const.DATE_NAME: [datetime.now(), datetime.now() - timedelta(days=1)],
                const.POLAR_NAME: [1, 1],
            }
        )
        res = get_date(data)
        self.assertIsInstance(res[0], datetime)
        self.assertEqual(2, len(res))

        data = pd.DataFrame(
            {
                const.DATE_NAME: [
                    datetime.now(),
                    datetime.now() + timedelta(seconds=1),
                ],
                const.POLAR_NAME: [1, 1],
            }
        )

        res = get_date(data)
        self.assertIsInstance(res[0], datetime)
        self.assertEqual(1, len(res))
