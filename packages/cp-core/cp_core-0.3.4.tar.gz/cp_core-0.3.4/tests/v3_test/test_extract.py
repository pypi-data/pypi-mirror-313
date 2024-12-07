import pandas as pd
import pytest

from cp_core.v3 import const, extract


@pytest.mark.v3
def test_obtain_night_data(get_df: pd.DataFrame):
    df = extract.obtain_night_data(get_df)
    assert set(["夜间通电电位(V_CSE)"]) <= set(df.keys())
