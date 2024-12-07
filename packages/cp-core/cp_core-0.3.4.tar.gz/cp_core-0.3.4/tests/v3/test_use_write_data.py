import pandas as pd

from cp_core.libs.total.controller import use_write_data


def test_use_write_data(tmp_folder):
    res = []
    write_data = use_write_data(1, "original", res.append, 1)
    write_data(pd.DataFrame(), "in_name", str(tmp_folder / "out_name.csv"))

    assert len(res) == 1
