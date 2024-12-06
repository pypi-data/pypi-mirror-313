import os
import unittest

from cp_core.config import csv_folder, project_root
from cp_core.libs.comprehensive.forms import InputData
from cp_core.libs.validator import schema


def ab_path(path):
    return os.path.join(project_root, csv_folder, path)


def _get_dict() -> dict:
    values = {
        "period": 4,
        "types": 0,
        "is_protect": 0,
        "device_id": "#11",
        "piece_id": "#11",
        "piece_area": 10.0,
        "resistivity": 10.0,
        "judge_metric": 10.0,
        "udl2_file": ab_path("data/filter/udl2_part.csv"),
        "udl1_file": ab_path("data/filter/udl2_part.csv"),
        "out_file_path_1": "C:\\Users\\Guest\\temp1.xls",
        "out_file_path_2": "C:\\Users\\Guest\\temp2.xls",
        "out_file_path_3": "C:\\Users\\Guest\\temp3.xls",
    }
    return values


def test_transfer():
    pass


def get_dict_p5():
    return {
        "period": 5,
        "corrosive": 1,
        "detect": 0,
        "is_protect": -1,
        "jiaoliu": 1,
        "zhiliu": 1,
        "output": "res.json",
    }


def test_parse_config_p5():
    v = get_dict_p5()
    res = schema.parse_config(v)
    assert isinstance(res, InputData)
    assert res is not None


class ConfigTestCase(unittest.TestCase):
    def test_parse_config(self):
        values = {
            "period": 1,
        }

        with self.assertRaises(Exception):
            res = schema.parse_config(values)
            self.assertIsInstance(res, dict)

        values = {
            "period": 1,
            "device_id": "#11",
            "resistivity": 10.0,
            "piece_id": "#11",
            "piece_area": 10.0,
            "file_path": ab_path("data/filter/udl2_part.csv"),
            "out_file_path": ab_path("temp/371#-5#-B123# udl2_sn-temp.csv"),
        }

        res = schema.parse_config(values)
        self.assertIsInstance(res, dict)

    def test_parse_config_p4(self):
        v = _get_dict()
        res = schema.parse_config(v)
        self.assertIsInstance(res, dict)

        v["udl1_path"] = ""
        res = schema.parse_config(v)
        self.assertIsInstance(res, dict)

    def test_parse_filter(self):
        prefix = project_root

        values = {
            "period": 1,
            "device_id": "#11",
            "resistivity": 10.0,
            "piece_id": "#11",
            "piece_area": 10.0,
            "file_path": ab_path("data/filter/udl2_part.csv"),
            "out_file_path": os.path.join(prefix, "temp/数据处理-123.xlsx"),
        }

        res = schema.validate_filter(values)
        self.assertIsInstance(res, dict)


if __name__ == "__main__":
    unittest.main()
