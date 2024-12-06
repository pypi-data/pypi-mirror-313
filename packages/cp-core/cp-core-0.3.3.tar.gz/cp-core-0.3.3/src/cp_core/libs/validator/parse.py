# coding: utf-8

from cp_core.libs.comprehensive.controller import (
    comprehensive_controller,
)
from cp_core.libs.core.filter.controller import filter_controller
from cp_core.libs.core.model.controller import model_controller
from cp_core.libs.core.stat.controller import stat_controller
from cp_core.libs.result import Result
from cp_core.libs.total.controller import compute_single


def transform_values(values: dict) -> dict:
    # for p2
    values["filtered_file"] = values.get("in_file_path")
    values["type_zhiliu"] = 0 if values.get("types") == 0 else 1
    return values


def get_pull_path(path: str) -> str:
    """返回值不变"""
    return path


def process_values(values: dict) -> Result:
    period = values.get("period")
    if not isinstance(period, int) or period < 1 or period > 5:
        raise TypeError(f"unknown peroid: {period}")

    values = transform_values(values)
    if period == 4:
        res, _ = compute_single(lambda: (-1, values), get_full_path=get_pull_path)
        return res
    elif period == 2:
        return stat_controller(values)
    else:
        parser = {
            1: filter_controller,
            3: model_controller,
            5: comprehensive_controller,
        }
        func = parser[period]
        return func(values)
