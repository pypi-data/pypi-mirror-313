import unittest
import pandas as pd
from .config import MetaName
from .libs import (
    mapping_to_by_dict,
    gen_tables,
    transform_data,
    compute_res,
    update_df_result,
)


class ControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.df = gen_tables()

    def test_update_df_result(self):
        df = update_df_result(self.df)
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_compute_res(self) -> None:
        df = compute_res(self.df)
        self.assertTrue((df[[MetaName.result]].any() != -10).any())

    def test_transform_data(self):
        df = transform_data(self.df)
        self.assertTrue((df.all() < 2).any())

    def test_handle_files(self):
        pass

    def test_mapping_to(self):
        normal_dict = {
            "消费": "中",
            "收入": "高",
            "疾病": "低",
            "吃饭": "有",
            "悲伤": "无",
            "玩": "过保护",
            "乐": "达标",
            "行": "欠保护",
        }

        res = mapping_to_by_dict(normal_dict)

        self.assertEqual(res["消费"], 0)
        self.assertEqual(res["收入"], 1)
        self.assertEqual(res["疾病"], -1)
        self.assertEqual(res["吃饭"], 1)
        self.assertEqual(res["悲伤"], 0)
        self.assertEqual(res["玩"], 1)
        self.assertEqual(res["乐"], 0)
        self.assertEqual(res["行"], -1)
        self.assertTrue("output" in res.keys())
