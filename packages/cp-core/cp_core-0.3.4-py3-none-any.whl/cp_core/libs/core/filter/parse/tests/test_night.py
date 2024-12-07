import unittest

import pandas as pd

from cp_core.libs.core.filter.forms import InputData
from cp_core.libs.core.filter.parse.merge import (
    get_merge_data_from_udl2,
)
from cp_core.libs.core.filter.parse.night import add_column_data, add_night_data
from cp_core.tests.path import udl2_path


class AddColumnTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(udl2_path, encoding="gbk")

    def test_add_night_data(self):
        values = InputData(
            **{
                "device_id": "371",
                "resistivity": "11",
                "piece_id": "B123",
                "piece_area": "1.0",
            },
            udl1_file="",
            udl2_file="",
            out_file_path="",
        )

        merge_all = get_merge_data_from_udl2(self.data, area=1.0)
        self.assertFalse(merge_all.empty)

        def fn(data: pd.DataFrame):
            return add_column_data(
                data,
                values,
                need=["piece_area", "piece_id", "resistivity", "device_id"],
                names=["试片面积(cm^2)", "试片编号", "土壤电阻率(Ω*m)", "测试桩编号"],
            )

        res = add_night_data(merge_all, fn)
        self.assertFalse(res.empty)
