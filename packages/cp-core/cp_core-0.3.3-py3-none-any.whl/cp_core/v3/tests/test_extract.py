import pandas as pd

from cp_core.v3 import extract
from cp_core.v3.tests.assert_fn import assert_keys
from cp_core.v3.tests.udl2_inputdata import get_df


def test_obtain_night_data():
    df = extract.obtain_night_data(get_df())
    # df.to_csv("./tmp/night_data.csv", index=False)
    assert assert_keys(df, ["夜间通电电位(V_CSE)"]), df.keys()
