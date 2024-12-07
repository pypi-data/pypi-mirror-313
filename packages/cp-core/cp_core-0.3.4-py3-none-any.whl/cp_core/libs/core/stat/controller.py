# coding: utf-8
# author: svtter
# time:
""" """

import functools
import os

from cp_core.exception import ValidateError
from cp_core.libs import types as T
from cp_core.libs.result import Result, Status
from cp_core.shared.judge import is_zhiliu
from cp_core.utils import is_windows

from . import file, merge, proto

# from .file import get_filtered_file, load_file, write_file
from .parse.ac_value import get_night_value, get_resistivity


def load_event(fname: str, values: dict) -> dict:
    data = file.load_file(fname)
    resistivity = get_resistivity(data)

    if is_zhiliu(values):
        night_value = get_night_value(data) if not values.get("is_protect") else -0.85
        res = {
            "resistivity_second": resistivity,
            "night_value": night_value,
        }

    else:
        res = {
            "resistivity_second": resistivity,
        }
    return res


def check_value(values: T.StatParams):
    if not values.get("filtered_file"):
        raise ValidateError("Input values has no `filtered_file` key")
    values["judge_metric"] = float(values["judge_metric"])
    return values


def validate_value(func):
    @functools.wraps(func)
    def wrapper(values: T.StatParams, *args, **kwargs) -> Result:
        try:
            values = check_value(values)
        except ValidateError as e:
            return Result(status=Status.failed, msg=str(e))
        return func(values, *args, **kwargs)

    return wrapper


@validate_value
def stat_controller(
    values: T.StatParams,
    process_data: proto.ProcessData = merge.generate_df_from_files,
) -> Result:
    """a controller is a api integration"""
    files = file.get_filtered_file(values)
    df = process_data(
        files,
        values=values,
        interval_jihua=values.get("interval_jihua", True),
    )
    file.write_file(
        df,
        old_filename=files[0],
        target_filename=values.get("out_file_path", ""),
        values=values,
    )

    return Result(status=Status.success, msg="success")


def check_event(values):
    import pathlib
    import subprocess

    p = pathlib.Path(file.get_filtered_file(values)[0])
    if is_windows():
        subprocess.Popen(f'explorer /select,"{p}"')
    else:
        os.system(f'open "{p.parent}"')
