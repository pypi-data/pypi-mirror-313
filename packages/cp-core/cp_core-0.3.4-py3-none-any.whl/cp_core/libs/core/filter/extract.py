"""
wrap the parse lib.

"""

import typing as t

import pandas as pd

from . import forms
from .errors import FilterError
from .parse import merge, night


def use_add_column(params):
    """generate a function to add data, for night column."""

    def wrapper(data):
        return night.add_column_data(
            data,
            params,
            need=["piece_area", "piece_id", "resistivity", "device_id"],
            names=["试片面积(cm^2)", "试片编号", "土壤电阻率(Ω*m)", "测试桩编号"],
        )

    return wrapper


@forms.validate_udl2
def extract_data_from_udl2(
    data: pd.DataFrame,
    params: forms.InputData,
    add_night=night.add_night,
) -> pd.DataFrame:
    """udl2 data extraction function"""
    data = merge.get_merge_data_from_udl2(data, params.piece_area)

    add_column_data = use_add_column(params)
    data = add_column_data(data)
    data = add_night(data)
    return data


def extract_data_from_udl1(
    types: str,
    udl2_data: pd.DataFrame,
    second_data: pd.DataFrame,
    params: forms.InputData,
) -> pd.DataFrame:
    """
    从 udl1 或者 anko 文件中抽取数据
    :param types:
    :param udl2_data:
    :param second_data:
    :param params:
    :return:
    """
    if types == "udl1":
        data = merge.get_merge_data_from_udl1(udl2_data, second_data, params.piece_area)
    elif types == "Anko":
        data = merge.get_merge_data_from_anko(udl2_data, second_data, params.piece_area)
    else:
        raise FilterError(f"not such type. {types}")

    add_column_data = use_add_column(params)
    res_data = night.add_night_data(
        data,
        add_column_data,
    )
    return res_data
