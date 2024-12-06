import unittest
import functools
from cp_core.libs.core.checker import *


class CheckerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame({"a": [0, 1], "b": [1, 0]})

    def test_check_numbers(self):
        test_func = functools.partial(check_df_numbers, df=self.df[:1])
        self.assertRaises(ColumnError, test_func)


if __name__ == "__main__":
    unittest.main()
