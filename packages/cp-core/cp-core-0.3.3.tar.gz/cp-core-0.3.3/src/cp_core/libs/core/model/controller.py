# coding: utf-8

import os
import typing as t

import pandas as pd

from cp_core.libs import types as T
from cp_core.libs.core.stat.merge import is_zhiliu
from cp_core.libs.result import Result, Status
from cp_core.shared.judge import is_protect

from . import file, predict


def handle_ac_dc_data(data, values: T.ModelParams) -> pd.DataFrame:
    if is_zhiliu(values):
        df = predict.predict_dc(data, is_protect(values))
    else:
        df = predict.predict_ac(data)
    return df


class ProcessData(t.Protocol):
    def __call__(self, data: pd.DataFrame, values: T.ModelParams) -> pd.DataFrame: ...


def model_controller(
    v: T.ModelParams, process_data: ProcessData = handle_ac_dc_data
) -> Result:
    data = file.load_file(v["in_file_path"])
    df = process_data(data, v)
    file.write_file(
        df,
        old_filename=v["in_file_path"],
        target_filename=v["out_file_path"],
        values=v,
    )
    return Result(status=Status.success, msg="success")


def view_event(values):
    import pathlib
    import subprocess

    from cp_core.utils import is_windows

    if is_windows():
        p = pathlib.Path(values.get("in_file_path"))
        subprocess.Popen(f'explorer /select,"{p}"')
    else:
        p = pathlib.Path(values.get("in_file_path"))
        os.system(f"open {p}")
