import os

import pytest

from cp_core.api import use_filter, use_model, use_stat
from cp_core.libs import types as T
from cp_core.libs.result import Status
from cp_core.tests.path import udl2_path
from test_record import RecordForTest


@pytest.fixture(scope="module")
def temp_test_dir():
    # Create a temporary directory
    yield "./tmp"


@pytest.fixture(scope="module")
def test_record():
    # Create a temporary directory
    return RecordForTest()


is_zhiliu = 0


def test_filter(temp_test_dir, test_record):
    test_params = T.FilterParams(
        type_zhiliu=is_zhiliu,
        device_id="#11",
        piece_id="#11",
        piece_area=10.0,
        resistivity=10.0,
        udl2_file=str(udl2_path),
        udl1_file="",
        out_file_path=os.path.join(temp_test_dir, "temp1.csv"),
    )
    r = use_filter(test_params)
    test_record.add_record(
        "test_filter",
        result=os.path.join(temp_test_dir, "temp1.csv"),
        details="nothing.",
    )
    assert r.status == Status.success


def test_use_stat(temp_test_dir):
    temp_dir = temp_test_dir
    params = T.StatParams(
        is_protect=True,
        type_zhiliu=is_zhiliu,
        resistivity=10.0,
        filtered_file=os.path.join(temp_dir, "temp1.csv"),
        judge_metric=10.0,
        # default is True, why ... forget. need to check git msg.
        interval_jihua=True,
        out_file_path=os.path.join(temp_dir, "temp2.csv"),
    )

    r = use_stat(params)
    assert r.status == Status.success


@pytest.mark.parametrize("is_zhiliu", [0, 1])
@pytest.mark.parametrize("is_protect", [0, 1])
def test_use_model(temp_test_dir, is_zhiliu, is_protect):
    temp_dir = temp_test_dir
    params = T.ModelParams(
        type_zhiliu=is_zhiliu,
        is_protect=is_protect,
        in_file_path=os.path.join(temp_dir, "temp2.csv"),
        out_file_path=os.path.join(temp_dir, "temp3.csv"),
    )
    r = use_model(params)
    assert r.status == Status.success
