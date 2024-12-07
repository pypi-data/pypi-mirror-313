import typing as t

import pandas as pd
import pytest

from cp_core.v3 import const, stat
from cp_core.v3.utils import to_df


@pytest.mark.v3
def test_avg_value(avg_data: pd.DataFrame):
    assert stat.get_avg_value(avg_data) != 1.0


def stage_2_result(stage_1_result: pd.DataFrame, is_zhiliu: int, is_protect: int):
    res = stat.get_all(
        stage_1_result,
        -0.85,
        {"type_zhiliu": is_zhiliu, "is_protect": is_protect},
        False,
    )
    return to_df([res])


@pytest.mark.v3
def test_avoid_insert(stage_1_result: pd.DataFrame):
    df = stage_2_result(stage_1_result, 0, 0)
    assert not set(const.DENSITY_VALUE_v1) <= set(df.keys())


@pytest.mark.v3
@pytest.mark.parametrize("is_zhiliu", [0, 1])
@pytest.mark.parametrize("is_protect", [0, 1])
def test_missing_vol(stage_1_result: pd.DataFrame, is_zhiliu: int, is_protect: int):
    df = stage_2_result(stage_1_result, is_zhiliu, is_protect)
    assert set(const.AC_VOL_VALUE) <= set(df.keys())


@pytest.mark.v3
@pytest.mark.parametrize("is_zhiliu", [0, 1])
@pytest.mark.parametrize("is_protect", [0, 1])
def test_stat(stage_1_result: pd.DataFrame, is_zhiliu: int, is_protect: int):
    df = stage_2_result(stage_1_result, is_zhiliu, is_protect)
    assert set([*const.AC_VOL_VALUE, *const.POLAR_NAME_LIST]) <= set(df.keys())


@pytest.mark.v3
def test_provide_get_metric():
    res = stat.provide_get_metric(
        {"type_zhiliu": 0, "is_protect": 1},
        1,
        pd.DataFrame({const.NIGHT_NAME: [1]}),
    )
    assert res() == 1


@pytest.mark.v3
def test_polar(stage_1_result: pd.DataFrame):
    values = {"type_zhiliu": 0, "is_protect": 0}

    res = stat.dc_value.polar(
        stage_1_result,
        True,
        interval_jihua=False,
        get_metric=stat.provide_get_metric(
            values, judge_metric=-0.85, data=stage_1_result
        ),
        polar_percent_func=stat.polar_percent_v2,
    )

    assert set(const.POLAR_NAME_LIST) <= set(find_in_keys(res))


def find_in_keys(key_list: list[tuple[str, t.Any]]) -> list[str]:
    """返回 key_list 中的所有 key"""
    return [key for key, _ in key_list]
