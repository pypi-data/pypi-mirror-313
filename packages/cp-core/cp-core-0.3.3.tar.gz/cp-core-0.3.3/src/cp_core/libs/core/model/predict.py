# code: utf-8

import typing as t

import pandas as pd

from . import judge, value
from .parse.const import ac as const_ac
from .parse.const import dc as const_dc


def predict_dc(
    data: pd.DataFrame,
    is_protect: bool,
    judge_risk_fn: t.Callable = judge.judge_risk_dc,
) -> pd.DataFrame:
    """
    获取全部的直流数据以及评判准则
    :param data:
    :param is_protect:
    :return:
    """

    # generate header of sheet.
    name_list = [
        const_dc.TEST_ID_NAME,
        const_dc.PIECE_ID_NAME,
        const_dc.PIECE_AREA_NAME,
        *value.gen_minmax_from_name(const_dc.POWERON_NAME),
        *value.gen_minmax_from_name(const_dc.POLAR_NAME),
    ]

    if is_protect:
        name_list.extend(
            const_dc.POLAR_VALUE_WITH_PROTECT,
        )
    else:
        name_list.extend(
            const_dc.POLAR_VALUE_WITHOUT_PROTECT,
        )

    df = data[name_list]
    risk = judge_risk_fn(df, is_protect)
    df[const_ac.RISK_ASSESS_NAME] = risk
    return df


def predict_ac(
    data: pd.DataFrame,
    judge_risk_fn: t.Callable = judge.judge_risk_ac,
) -> pd.DataFrame:
    """
    获取全部的交流数据以及评判准则
    :param data:
    :return:
    """
    df = data[
        [
            const_ac.TEST_ID_NAME,
            const_ac.PIECE_ID_NAME,
            const_ac.PIECE_AREA_NAME,
            *value.gen_minmax_from_name(const_ac.POWERON_NAME),
            *value.gen_minmax_from_name(const_ac.POLAR_NAME),
            *const_ac.AC_DENSE_VALUE,
            *const_ac.POLAR_VALUE,
            *const_ac.DC_DENSE_VALUE,
        ]
    ]
    risk = judge_risk_fn(df)
    df[const_ac.RISK_ASSESS_NAME] = risk
    return df
