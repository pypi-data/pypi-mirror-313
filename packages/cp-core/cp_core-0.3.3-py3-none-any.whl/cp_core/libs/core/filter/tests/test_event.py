import os
import unittest
from typing import Iterable

import pandas as pd
from pydantic import ValidationError

from cp_core.config import project_root
from cp_core.libs.core.filter import errors
from cp_core.libs.core.filter.controller import (
    process_data,
    validate_config,
)

# from cp_core.libs.core.filter.extract import check_data
from cp_core.libs.core.filter.forms import InputData
from cp_core.tests.path import csv_folder, test2


def check_data(data, types: str):
    """This function is used to check the format of the udl2, udl1 file.
    TODO: not finished. Only for test.
    :param data:
    :param types:
    :return:
    """
    # list for checker
    res: tuple = (
        ("udl2", None),
        ("udl1", "error data."),
    )

    res = dict(iter(res))
    return res[types]


class ConfigTest(unittest.TestCase):
    def test_process_data_v2(self):
        for v in values_list():
            assert v.udl2_file, v
            try:
                r = process_data(v)
                self.assertIsNotNone(r)
                self.assertLess(1, len(r.index), msg=v)
            except errors.FileError as e:
                self.fail(str(e) + f"\n{v}")

    def test_config(self):
        """
        :return:
        """
        values = {
            "device_id": "371",
            "resistivity": "",
            "piece_id": "B123",
            "piece_area": 1,
        }
        with self.assertRaises(ValidationError):
            res = validate_config(values)
            assert res is None

    def test_before_trans(self):
        values = {
            "device_id": "371",
            "resistivity": "11",
            "piece_id": "B123",
            "piece_area": "1.0",
        }
        with self.assertRaises(ValidationError):
            res = validate_config(values)
            assert res is None

    def test_after_trans(self):
        values = {
            "udl2_file": "123",
            "device_id": "371",
            "resistivity": 11,
            "piece_id": "B123",
            "piece_area": 1.0,
            "out_file_path": "123",
        }
        validate_config(values)

    @unittest.skip("Not finished.")
    def test_invalid_input(self):
        udl2_data = pd.read_csv(test2.get("udl2_path"), encoding="gbk")
        udl1_data = pd.read_csv(test2.get("udl1_invalid"), encoding="gbk")

        msg = check_data(udl2_data, types="udl2")
        self.assertIsNone(msg)

        msg = check_data(udl1_data, types="udl1")
        self.assertEqual(msg, "error data.")

        self.fail("not finished")


def ab_path(path):
    return os.path.join(project_root, path)


def values_list() -> Iterable[InputData]:
    path_list = (
        (f"{csv_folder}/data/filter/udl2_part.csv", ""),
        (
            f"{csv_folder}/data/filter/udl2+udl1/udl2.csv",
            f"{csv_folder}/data/filter/udl2+udl1/udl1.csv",
        ),
        (
            f"{csv_folder}/data/filter/udl2+anko/udl2.csv",
            f"{csv_folder}/data/filter/udl2+anko/Anko.csv",
        ),
    )

    for v1, v2 in path_list:
        values = InputData(
            **{
                "udl2_file": ab_path(v1),
                "udl1_file": ab_path(v2) if v2 else "",
                "device_id": 10,
                "resistivity": 10.0,
                "piece_id": 1,
                "piece_area": 10.0,
            },
            out_file_path="",
        )
        yield values
