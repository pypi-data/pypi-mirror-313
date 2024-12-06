import os
import unittest

from cp_core.libs import types as T
from cp_core.libs.total import controller as c
from cp_core.libs.total import fileutils as f
from cp_core.tests.path import udl2_path


class EventTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_config: T.Params = {
            "period": 4,
            "types": 0,
            "type_zhiliu": 0,
            "is_protect": 0,
            # "current_type": 1,
            "device_id": "#11",
            "piece_id": "#11",
            "piece_area": 10.0,
            "resistivity": 10.0,
            "judge_metric": 10.0,
            "udl2_file": str(udl2_path),
            "udl1_file": "",
            "interval_jihua": False,
            "out_file_path_1": "temp1.csv",
            "out_file_path_2": "temp2.csv",
            "out_file_path_3": "temp3.csv",
        }
        self.test_config["type_zhiliu"] = self.test_config["types"]

    def return_fn(self):
        def get_full_path(path: str):
            return os.path.join("./tmp", path)

        return get_full_path

    def test_total(self):
        # if zhiliu, 0, else 1.
        get_full_path = self.return_fn()

        r, df = c.compute_single(self.get_id_and_params, get_full_path)
        assert r.is_success()
        assert df is not None

    def get_id_and_params(self):
        return 0, self.test_config

    def test_merge_files(self):
        c_list = []
        df_list = []

        get_full_path = self.return_fn()

        for i in range(3):
            temp_c = self.test_config.copy()
            temp_c["out_file_path_3"] = f"temp-11-{i}.csv"
            r, df = c.compute_single(self.get_id_and_params, get_full_path)
            df_list.append(df)
            c_list.append(r)

        df = f.merge_files(c_list, df_list)
