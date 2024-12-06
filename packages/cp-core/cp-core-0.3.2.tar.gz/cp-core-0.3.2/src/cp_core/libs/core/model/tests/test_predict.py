# coding: utf-8
import os
import unittest

from cp_core.config import project_root
from cp_core.libs.core.model.file import load_file
from cp_core.libs.core.model.predict import predict_dc
from cp_core.tests.path import csv_folder


class MergeTest(unittest.TestCase):
    def setUp(self) -> None:
        prefix = os.path.join(project_root, csv_folder, "data/model")
        filename = r"zhiliu-protect.xlsx"
        filename = os.path.join(prefix, filename)
        self.zhiliu_data = load_file(filename)

    def test_something(self):
        res = predict_dc(self.zhiliu_data, is_protect=True)
        print(res)
