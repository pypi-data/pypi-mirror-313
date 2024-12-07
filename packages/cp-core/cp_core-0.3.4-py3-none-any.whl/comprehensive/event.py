# coding: utf-8

import time
import pathlib
import subprocess
from cp_core.utils import is_windows
from cp_core.libs.comprehensive.controller import (
    comprehensive_controller,
)
from comprehensive.config import MetaKey
from comprehensive.libs import (
    mapping_to_by_dict,
    change_text,
    gen_tables,
    trans_back,
    open_file,
    update_df_result,
    write_file,
)


def file_event(values: dict) -> str:
    """文件事件，可能包含异常，反馈给上层用户

    Args:
        values (dict): _description_

    Returns:
        str: _description_
    """
    file_path = values.get(MetaKey.file)
    if not isinstance(file_path, str):
        return f"error file name: {file_path}"

    try:
        df = open_file(file_path)
    except Exception as e:
        return f"File error. error is: {e}"

    df = update_df_result(df)
    write_file(df, file_path + f"-{int(time.time())}.csv")
    return "Finished with file."


def option_event(values: dict, window) -> str:
    values = mapping_to_by_dict(values)
    if values:
        result = comprehensive_controller(values=values, write=False)
    else:
        return f"Bad values: {values}"
    val = trans_back(result.value)
    change_text(window, MetaKey.result, val)
    return f"Finished: {val}"


def confirm_event(values, window) -> str:
    if not values.get(MetaKey.file):
        return option_event(values, window)
    else:
        return file_event(values)


def view_event(values, key):
    """
    view file in explorer
    """
    if is_windows():
        p = pathlib.Path(values.get(key))
        subprocess.Popen(f'explorer /select,"{p}"')
    else:
        p = pathlib.Path(values.get(key))
        subprocess.Popen(f"open {p}")


def gen_event():
    df = gen_tables()
    write_file(df, "temp.csv")
