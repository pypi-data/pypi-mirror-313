import pandas as pd
import pytest

from cp_core.libs.types import ModelParams
from cp_core.v3.const import POLAR_NAME_LIST
from cp_core.v3.funcset import FuncSetV3
from cp_core.v3.utils import to_df
from tests.v3_test.assert_fn import assert_keys
from tests.v3_test.udl2_inputdata import params


@pytest.mark.v3
@pytest.mark.parametrize("is_zhiliu", [0, 1])
@pytest.mark.parametrize("is_protect", [0, 1])
def test_funcset_stat(stage_1_result: pd.DataFrame, is_zhiliu: int, is_protect: int):
    funcset = FuncSetV3()

    def try_normal_cols(df):
        assert set(
            [
                "通电电位(V_CSE)_min",
                "通电电位(V_CSE)_max",
                "夜间通电电位(V_CSE)_min",
                "夜间通电电位(V_CSE)_max",
            ]
        ) <= set(df.keys())
        assert set(POLAR_NAME_LIST) <= set(df.keys())

    def write_file(is_zhiliu, is_protect):
        with open(
            f"./tmp/stage-2-result-{'ac' if is_zhiliu == 0 else 'dc'}-protect-{is_protect}.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(df.keys()))

    params["type_zhiliu"] = is_zhiliu
    params["is_protect"] = is_protect

    df_list = [
        funcset.stat(
            stage_1_result,
            params=params,
            interval_jihua=params["interval_jihua"],
        )
    ]

    df = to_df(df_list)

    df.to_csv(
        f"./tmp/stage-2-result-{'ac' if is_zhiliu == 0 else 'dc'}-protect-{is_protect}.csv",
        index=False,
    )

    write_file(is_zhiliu, is_protect)
    try_normal_cols(df)


@pytest.mark.v3
@pytest.mark.parametrize("is_zhiliu", [0, 1])
@pytest.mark.parametrize("is_protect", [0, 1])
def test_funcset_model(stage_2_result: pd.DataFrame, is_zhiliu: int, is_protect: int):
    funcset = FuncSetV3()
    values = ModelParams(
        type_zhiliu=bool(is_zhiliu),
        is_protect=bool(is_protect),
        in_file_path="",
        out_file_path="",
    )

    df = funcset.model(stage_2_result, values=values)
    df.to_csv(
        f"./tmp/stage-3-result-{'ac' if is_zhiliu == 0 else 'dc'}-protect-{is_protect}.csv",
        index=False,
    )
    assert assert_keys(df, ["测试桩编号"])
