import unittest

import pandas as pd

from cp_core.libs.core.filter.parse.anko_ac import ac_reading_from_anko
from cp_core.libs.core.filter.parse.const import AC_VOL_NAME, pAC
from cp_core.libs.core.filter.parse.date import str2datetime_first_time
from cp_core.libs.core.filter.parse.feature import (
    compare_interference_vol,
)
from cp_core.libs.core.filter.parse.merge import (
    filter_potential_ac_reading,
)
from cp_core.libs.core.filter.parse.udl1_ac import ac_reading_from_udl1
from cp_core.libs.core.filter.utils import FeatureUtils


class FeatureTest(unittest.TestCase):
    feature_utils = FeatureUtils()

    def setUp(self) -> None:
        self.udl2_data = self.feature_utils.udl2_sample_data()
        self.anko_data = self.feature_utils.anko_sample_data()
        self.udl1_data = self.feature_utils.udl1_sample_data()

    def test_return_type(self):
        udl2_data, start = str2datetime_first_time(self.udl2_data)
        potential_ac_df_udl1 = ac_reading_from_anko(self.anko_data, start)
        potential_ac_df_udl2 = filter_potential_ac_reading(udl2_data, start)
        interference_vol = compare_interference_vol(
            potential_ac_df_udl2, potential_ac_df_udl1
        )
        self.assertIsInstance(interference_vol, pd.Series)

    def test_compare_interference_vol(self):
        """
        Test interference vol
        Returns
        -------

        """

        udl2_data, start = str2datetime_first_time(self.udl2_data)
        potential_ac_df_anko = ac_reading_from_anko(self.anko_data, start)
        potential_ac_df_udl2 = filter_potential_ac_reading(udl2_data, start)

        interference_vol = compare_interference_vol(
            potential_ac_df_udl2, potential_ac_df_anko
        )

        self.assertEqual(
            potential_ac_df_anko[AC_VOL_NAME].any(), interference_vol.any()
        )
        # udl2_data[pAC_NAME] = interference_vol

        potential_ac_df_udl1 = ac_reading_from_udl1(self.udl1_data, start=start)
        interference_vol = compare_interference_vol(
            potential_ac_df_udl2, potential_ac_df_udl1
        )

        self.assertEqual(
            potential_ac_df_udl1[AC_VOL_NAME].any(), interference_vol.any()
        )
