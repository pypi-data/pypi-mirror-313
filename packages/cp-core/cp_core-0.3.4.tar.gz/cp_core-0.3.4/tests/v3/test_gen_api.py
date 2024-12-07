import pytest

from cp_core.libs.gen_api import get_steps
from cp_core.libs.types import FilterParams, StatParams
from cp_core.v3.funcset import FuncSetV3


@pytest.fixture
def fn():
    use_filter, use_stat, use_model = get_steps(FuncSetV3())
    return use_filter, use_stat, use_model


def test_stat(fn):
    _, use_stat, _ = fn
    use_stat(
        StatParams(
            is_protect=True,
            type_zhiliu=True,
        )
    )


def test_filter(fn):
    use_filter, _, _ = fn
    use_filter(
        FilterParams(
            type_zhiliu=True,
            device_id="test-device",
            piece_id="test-piece",
            piece_area=10.0,
            resistivity=10.0,
            udl2_file="test.csv",
            udl1_file="",
            out_file_path="output.csv",
        )
    )
