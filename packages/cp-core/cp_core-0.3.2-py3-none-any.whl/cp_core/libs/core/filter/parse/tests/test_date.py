import os
import unittest
from cp_core.libs.core.filter.parse.date import *
from cp_core.libs.core.filter.parse.const import *
from cp_core.tests.path import udl2_path
from cp_core.config import project_root, csv_folder
from cp_core.libs.core.checker import check_df_numbers


class DateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.read_csv(udl2_path, encoding="gbk")

        data_path = (
            udl2_path,
            os.path.join(project_root, csv_folder, "data/filter/udl2_DW06-20057.csv"),
        )

        self.data_list = (pd.read_csv(path, encoding="gbk") for path in data_path)

    def test_date(self):
        for data in self.data_list:
            data = str2datetime(data)
            self.assertIsInstance(data[DATE_NAME].iloc[0], pd.Timestamp)

    def test_get_first_time(self):
        data = str2datetime(self.data)
        self.assertLess(1, len(data.index))
        start = get_first_time(data)
        self.assertEqual("07-25-2019 09:45:02", start)

    def test_locate_time(self):
        for data in self.data_list:
            df = str2datetime(data)
            start = get_first_time(df)
            self.assertLess(1, len(df.index))

            df = data.loc[data["Record Type"] == CC_AC_READING]
            empty = False
            if len(df.index) < 1:
                empty = True

            df = locate_time(df, first_time=start)
            if not empty:
                self.assertLess(1, len(df.index))


if __name__ == "__main__":
    unittest.main()
