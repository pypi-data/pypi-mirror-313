# coding: utf-8

import os
import unittest
from pathlib import Path

from cp_core.config import project_root
from cp_core.libs.core.filter.errors import FileError
from cp_core.libs.core.filter.fileutils import (
    get_file_type,
    read_first_file,
)
from cp_core.tests.path import csv_folder, test3
from cp_core.utils import is_windows


class FileTest(unittest.TestCase):
    def test_read_file(self):
        if not is_windows():
            return

        table = (
            (
                os.path.join(
                    project_root, "addtional_data_for_material", r"temp\for_file_1.csv"
                ),
                FileError.not_found,
            ),
            (
                os.path.join(
                    project_root, f"{csv_folder}/data/filter/udl2+anko/Anko.csv"
                ),
                FileError.not_found_udl2,
            ),
        )

        for path, res in table:
            with self.assertRaises(FileError) as e:
                read_first_file(path)
                self.assertEqual(e.exception.message, res)

    def test_temp_file(self):
        path = os.path.join(project_root, csv_folder, "data/filter/udl2_part.csv")
        data = read_first_file(path)
        self.assertIsNotNone(data)

    def test_parent_name(self):
        path = Path(test3.get("anko_path"))
        self.assertIsNotNone(path)

    def test_get_file_types(self):
        table = (
            ("Anko.csv", "Anko"),
            ("udl1.csv", "udl1"),
        )

        for fname, label in table:
            res = get_file_type(fname)
            self.assertEqual(res, label)

        with self.assertRaises(FileError):
            error_list = ("anko.csv", "non.csv", "udl2.csv")
            for error_filename in error_list:
                get_file_type(error_filename)
