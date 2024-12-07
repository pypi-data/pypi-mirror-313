import pytest

from cp_core.libs import types as T
from cp_core.libs.core.filter import controller


def test_filter_controller():
    values = T.FilterParams(
        type_zhiliu=True,
        device_id="123",
        resistivity=1.0,
        piece_id="123",
        piece_area=1.0,
        udl2_file="123",
        out_file_path="123",
    )
    res = controller.filter_controller(values)
    print(res)
