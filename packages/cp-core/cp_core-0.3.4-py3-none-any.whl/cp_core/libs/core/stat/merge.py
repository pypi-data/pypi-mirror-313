# coding: utf-8
# author: svtter
# time:
""" """

import typing as t

import pandas as pd

from cp_core.libs import types as T
from cp_core.shared.judge import is_zhiliu

from . import forms
from .file import load_file
from .parse import ac_value, dc_value
from .parse.ac_value import get_value
from .parse.const.ac import (
    PIECE_AREA_NAME,
    PIECE_ID_NAME,
    TEST_ID_NAME,
)


class FuncSet:
    """stat 使用的 funcset，可以被其他的方法替代"""

    @classmethod
    def is_dc(cls, values: T.Params):
        return is_zhiliu(values)

    @classmethod
    def get_all_func(cls, values: T.Params) -> t.Callable:
        """根据不同的电流，返回不同的处理方法"""
        if cls.is_dc(values):
            return dc_value.get_all
        else:
            return ac_value.get_all


@forms.check_value(name="judge_metric")
def generate_row_from_data(
    data: pd.DataFrame,
    values: T.Params,
    interval_jihua: bool,
    func_set: t.Type[FuncSet] = FuncSet,
) -> list:
    """
    从 original data 中生成列
    :param data:
    :param values:
    :return:
    """
    # 获取测试id，桩号，桩区
    name_list = (TEST_ID_NAME, PIECE_ID_NAME, PIECE_AREA_NAME)
    res1: list[list[str | int | float]] = [
        [name, get_value(data, name)] for name in name_list
    ]

    get_all = func_set.get_all_func(values)

    df = get_all(
        data,
        judge_metrics=values["judge_metric"],
        values=values,
        interval_jihua=interval_jihua,
    )
    # 实际上就一条数据
    res = [*res1, *df]
    return res


def generate_df_from_files(
    files: tuple[str, ...],
    values,
    interval_jihua: bool,
    generate_row: t.Callable = generate_row_from_data,
) -> pd.DataFrame:
    """
    从多个文件中生成列
    :param files:
    :param values:
    :return:
    """
    df_list: list[pd.DataFrame] = [load_file(name) for name in files]
    rows = (generate_row(df, values, interval_jihua=interval_jihua) for df in df_list)

    # generate data frame
    res = (dict(iter(row)) for row in rows)
    df = pd.DataFrame(res)
    return df
