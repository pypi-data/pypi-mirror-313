import typing as t

import pandas as pd

from cp_core.libs.core.model import predict

from . import const


def judge_risk_ac(data: pd.DataFrame) -> str:
    """以后可以用具体的变量去替代"""
    high, mid, low, missing = const.RISK_ASSESS_VALUE_V3
    NEGATIVE_005_03 = const.POLAR_NAME_LIST[-1]

    # if data[const.AC_DENSITY_VALUE[-1]].empty:
    #     return missing

    if data[const.AC_DENSITY_VALUE[-1]].values[0] > 0.9:
        return low

    if (
        data[const.AC_DENSITY_VALUE_0_100].values[0] > 0.9
        and data[NEGATIVE_005_03].values[0] > 0.9
    ):
        return low

    return high


def predict_ac(
    data: pd.DataFrame,
    judge_risk_fn: t.Callable = judge_risk_ac,
) -> pd.DataFrame:
    """
    获取全部的交流数据以及评判准则
    :param data:
    :return:
    """
    df = data[
        [
            const.TEST_ID_NAME,
            const.PIECE_ID_NAME,
            const.PIECE_AREA_NAME,
            const.AC_DENSITY_VALUE[-1],
            const.POLAR_005_03,
        ]
    ]

    df[const.AC_DENSITY_VALUE_0_100] = (
        data[const.AC_DENSITY_VALUE[-1]] + data[const.AC_DENSITY_VALUE[-2]]
    )

    risk = judge_risk_fn(df)
    df[const.RISK_ASSESS_NAME] = risk

    df = df.reindex(
        columns=[
            const.TEST_ID_NAME,
            const.PIECE_ID_NAME,
            const.PIECE_AREA_NAME,
            const.AC_DENSITY_VALUE[-1],
            const.AC_DENSITY_VALUE_0_100,
            const.POLAR_005_03,
            const.RISK_ASSESS_NAME,
        ]
    )

    return df


def judge_risk_dc(data: pd.DataFrame, is_protect: bool):
    high, mid, low, missing = const.RISK_ASSESS_VALUE_V3

    if is_protect:
        if data[const.POLAR_NAME_LIST[0]].empty:
            return missing
        if (
            data[const.POLAR_NAME_LIST[0]].values[0] <= 0.1
            and data[const.POLAR_NAME_LIST[1]].values[0] <= 0.05
            and data[const.POLAR_NAME_LIST[2]].values[0] <= 0.01
        ):
            return low

        if (
            data[const.POLAR_NAME_LIST[0]].values[0] > 0.2
            and data[const.POLAR_NAME_LIST[1]].values[0] > 0.15
            and data[const.POLAR_NAME_LIST[2]].values[0] > 0.1
        ):
            return high
        return mid
    else:
        if data[const.POLAR_NIGHT_20MV].empty:
            return missing
        night_20mv_v = data[const.POLAR_NIGHT_20MV].values[0]
        if night_20mv_v <= 0.05:
            return low
        elif night_20mv_v > 0.05 and night_20mv_v <= 0.15:
            return mid
        return high  # > 0.15


def predict_dc(data: pd.DataFrame, is_protect: bool = False) -> pd.DataFrame:
    """
    获取全部的直流数据以及评判准则
    :param data:
    :param is_protect:
    :return:
    """

    # generate header of sheet.
    name_list = [
        const.TEST_ID_NAME,
        const.PIECE_ID_NAME,
        const.PIECE_AREA_NAME,
        *predict.value.gen_minmax_from_name(const.POWER_ON_NAME),
        *predict.value.gen_minmax_from_name(const.POLAR_NAME),
    ]

    if is_protect:
        name_list.extend(const.POLAR_NAME_LIST[:4])
    else:
        name_list.append(const.POLAR_NIGHT_20MV)

    df = data[name_list]
    risk = judge_risk_dc(df, is_protect)
    df[const.RISK_ASSESS_NAME] = risk
    return df
