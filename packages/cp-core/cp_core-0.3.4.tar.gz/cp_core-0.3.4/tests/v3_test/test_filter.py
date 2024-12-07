import pytest

from cp_core.v3 import const
from cp_core.v3.funcset import FuncSetV3
from tests.v3_test.udl2_inputdata import values


@pytest.mark.v3
def test_funcset_filter():
    funcset = FuncSetV3()

    # 这里没有用到 values 的 udl2-filename
    df = funcset.filter(values)
    df.to_csv("./tmp/stage-1-result.csv", index=False)
    assert set([const.NIGHT_POWERON, const.NIGHT_NAME, "状态"]) <= set(df.keys())
    assert const.NIGHT_NAME_OLD not in set(df.keys())
