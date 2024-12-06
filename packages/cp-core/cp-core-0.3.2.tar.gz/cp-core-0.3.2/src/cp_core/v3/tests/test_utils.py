from cp_core.v3.utils import to_df


def test_to_df():
    df_list = [[["hello", 1.0], ["world", 2.0], ["test", 3.0]]]
    df = to_df(df_list)
    assert df["hello"][0] == 1.0
    assert df["world"][0] == 2.0
