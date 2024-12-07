import typing as t

import pandas as pd

from cp_core.libs import types as T
from cp_core.libs.core.stat.merge import FuncSet
from cp_core.libs.core.stat.parse import ac_value, dc_percent, dc_value, percent

from . import const


class StatFuncSetV3(FuncSet):
    @classmethod
    def get_all_func(cls, values: T.Params) -> t.Callable:
        """只使用 DC 的处理方法"""
        return get_all


def provide_get_metric(
    values: dict,
    judge_metric: float,
    data: pd.DataFrame,
):
    def get_metric():
        if values["type_zhiliu"] == 0:
            return get_avg_value(data)

        if values["is_protect"]:
            return judge_metric
        return get_avg_value(data)

    return get_metric


@dc_value.convert_datetime
def get_all(
    data: pd.DataFrame,
    judge_metrics: float,
    values: dict,
    interval_jihua: bool,
) -> list:
    def get_metric():
        if values["type_zhiliu"] == 0:
            return get_avg_value(data)

        if values["is_protect"]:
            return judge_metrics
        return get_avg_value(data)

    res = [
        *dc_value.get_night_value(data, types="poweron"),
        *dc_value.get_night_value(data, types="polar"),
        (const.JUDGE_METRIC_NAME, judge_metrics),
        *dc_value.poweron(data),
        *dc_value.polar(
            data,
            values["is_protect"],
            interval_jihua=interval_jihua,
            get_metric=get_metric,
            polar_percent_func=polar_percent_v2,
        ),
        *ac_value.ac_voltage(data),
        # *dc_value.density(data),
        *dc_density(data),
        *dc_value.ac_vol(data),
        *ac_value.ac_density(data),
    ]

    return res


def dc_density(data: pd.DataFrame):
    res = [
        *dc_value.get_max_min_average(const.DC_DENSITY_NAME, data),
        *dc_percent.density(data[const.DC_DENSITY_NAME]),
    ]
    return res


def get_avg_value(df: pd.DataFrame) -> float:
    """返回 const.NIGHT_NAME 的第一个数值"""
    return df[const.NIGHT_NAME].iloc[0]


def polar_percent_v2(
    se,
    metric,
    is_protect,
) -> list:
    """
    极化电位
    """
    name = const.POLAR_NAME_LIST
    percents = [
        percent.get_count(se, se > metric),
        percent.get_count(se, se > metric + 0.05),
        percent.get_count(se, se > metric + 0.1),
        percent.get_count(se, se > metric + 0.85),
        percent.get_count(se, se > metric - 0.30),
        percent.get_count(se, se < metric - 0.05),
        percent.get_count(se, se < metric - 0.25),
        percent.get_count(se, se < metric - 0.3),
        percent.get_count(se, se < metric - 0.35),
        percent.get_count(se, se < metric - 0.4),
        percent.get_count(se, (se < metric - 0.05) & (se > metric - 0.3)),
        percent.get_count(se, se > metric + 0.02),
    ]

    assert len(name) == len(percents)
    res = [(name, val) for name, val in zip(name, percents)]
    return res
