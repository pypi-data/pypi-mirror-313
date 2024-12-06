# coding: utf-8
import unittest
import pandas as pd
from cp_core.utils import is_windows, read_csv


class FileTest(unittest.TestCase):
    @unittest.skip
    def test_temp_file(self):
        if not is_windows():
            return
        data = read_csv(
            r"C:\Users\Administrator\Documents\Github\material_process\temp\371#-5#-B123# udl2_sn020736.csv",
            encoding="gbk",
        )
        print(data)
