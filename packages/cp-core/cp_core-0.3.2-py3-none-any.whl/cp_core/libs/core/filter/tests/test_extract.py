"""
need import data
"""

import os
import unittest

import pandas as pd

from cp_core.config import csv_folder, project_root
from cp_core.libs.core.checker import check_col
from cp_core.libs.core.filter.extract import (
    extract_data_from_udl1,
    extract_data_from_udl2,
)
from cp_core.libs.core.filter.fileutils import open_anko_file
from cp_core.libs.core.filter.parse import const
from cp_core.libs.core.filter.parse.date import str2datetime
from cp_core.libs.core.filter.parse.tests.params import values
from cp_core.tests.path import test2, test3, udl2_path


class ExtractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(udl2_path, encoding="gbk")
        self.data2_path = os.path.join(
            project_root, csv_folder, "data/filter/udl2_DW06-20057.csv"
        )
        self.data_with_missing = pd.read_csv(self.data2_path, encoding="gbk")

    def test_extract_udl2(self):
        for data in (self.data, self.data_with_missing):
            data = extract_data_from_udl2(data, values)
            check_col(data, const.DATE_NAME)

    def test_status_udl2(self):
        for data in (self.data, self.data_with_missing):
            data = extract_data_from_udl2(data, values)
            check_col(data, const.STATUS_NAME)

    def test_extract_anko(self):
        udl2_data = pd.read_csv(test3.get("udl2_path"), encoding="gbk")
        anko_data = open_anko_file(test3.get("anko_path"))

        data = extract_data_from_udl1(
            types="Anko", udl2_data=udl2_data, second_data=anko_data, params=values
        )
        self.assertFalse(data.empty)

    def test_extract_udl1(self):
        udl2_data = pd.read_csv(test2.get("udl2_path"), encoding="gbk")
        udl1_data = pd.read_csv(test2.get("udl1_path"), encoding="gbk")

        udl2_data = str2datetime(udl2_data)
        data = extract_data_from_udl1(
            types="udl1", udl2_data=udl2_data, second_data=udl1_data, params=values
        )
        self.assertFalse(data.empty)
