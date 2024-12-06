# src\cp_core\libs\core\stat\parse\ac_percent.py
import typing as t

import pandas as pd

from cp_core.libs.core.stat.parse import ac_value, value
from cp_core.libs.core.stat.parse.ac_percent import polarization_point as percent
from cp_core.libs.total import types as T

from . import const, settings


def percent_v3(se, metric: float, settings: settings.DCSettings):
    return percent(
        se,
        metric,
        settings.polar_value,
        value_list=[
            (">", 0),
            (">", 0.05),
            (">", 0.1),
            (">", 0.85),
            ("<", -0.25),
            ("<", -0.3),
            ("<", -0.35),
            ("<", -0.4),
        ],
    )


def percent_v2(se, metric: float):
    return percent(
        se,
        metric,
        const.POLAR_VALUE,
        value_list=[
            (">", 0),
            (">", 0.05),
            (">", 0.1),
            (">", 0.85),
            ("<", -0.25),
            ("<", -0.3),
            ("<", -0.35),
            ("<", -0.4),
        ],
    )


def get_all_func(values: T.general.Params):
    def get_all(
        data: pd.DataFrame,
        judge_metrics: float,
        values: dict,
        interval_jihua: bool,
    ) -> list:
        res = [
            (const.JUDGE_METRIC_NAME, judge_metrics),
            *value.get_max_min_average(const.NIGHT_POWERON, data),
            *value.get_max_min_average(const.NIGHT_POLAR, data),
            *value.poweron(data),
            *ac_value.polar(data, judge_metric=judge_metrics, percent_func=percent_v2),
            *ac_value.dc_density(data),
            *ac_value.ac_voltage(data),
            *ac_value.ac_density(data),
        ]

        return res

    return get_all
