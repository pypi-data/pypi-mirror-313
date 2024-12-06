import unittest

from .base import get_data, FILE_PATH
from cp_core.libs.core.stat.merge import (
    generate_row_from_data,
    generate_df_from_files,
)


class MergeTest(unittest.TestCase):
    def test_merge(self):
        data = get_data()
        values = {"judge_metric": -0.85, "type_zhiliu": False}
        res = generate_row_from_data(data, values, True)
        for val in res:
            self.assertTrue(len(val) == 2, msg=val)
        print(res)

    def test_dataframe(self):
        values = {"judge_metric": -0.85, "type_zhiliu": False}

        res = generate_df_from_files((FILE_PATH,), values=values, interval_jihua=True)
        print(res)
