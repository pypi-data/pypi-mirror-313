# final judgement of risk of ac/dc data.

import typing as t

import pandas as pd

import cp_core.libs.types as T
from cp_core.libs.core.model import judge, value
from cp_core.libs.core.model.parse.const import ac as const_ac
from cp_core.libs.core.model.parse.const import dc as const_dc


def judge_risk_ac(data: pd.DataFrame) -> pd.DataFrame:
    risk = judge.judge_risk_ac(data)
    data[const_ac.RISK_ASSESS_NAME] = risk
    return data


def judge_risk_dc(data: pd.DataFrame, is_protect: bool):
    risk = judge.judge_risk_dc(data, is_protect)
    data[const_ac.RISK_ASSESS_NAME] = risk
    return data


def get_all_dc(data: pd.DataFrame, is_protect: bool):
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
        *const_dc.POLAR_VALUE_WITH_PROTECT,
    ]

    df = data[name_list]
    risk = judge_risk_dc(df, is_protect)
    df[const_ac.RISK_ASSESS_NAME] = risk
    return df


def get_all_ac(data: pd.DataFrame, params: T.Params):
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
    risk = judge_risk_ac(df)
    df[const_ac.RISK_ASSESS_NAME] = risk
    return df
