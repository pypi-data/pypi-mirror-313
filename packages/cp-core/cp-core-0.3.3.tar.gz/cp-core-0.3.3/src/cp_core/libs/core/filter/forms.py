from __future__ import annotations

import functools
import typing as t

import pandas as pd
from pydantic import BaseModel

from cp_core import config
from cp_core.libs import types as T

from . import errors


class InputData(BaseModel):
    device_id: str | int
    resistivity: float
    piece_id: str | int
    piece_area: float
    udl2_file: str
    udl1_file: str | None = None
    out_file_path: str

    @classmethod
    def from_dict(cls, values: T.Params) -> "InputData":
        return InputData(
            device_id=values["device_id"],
            resistivity=values["resistivity"],
            piece_id=values["piece_id"],
            piece_area=values["piece_area"],
            udl2_file=values["udl2_file"],
            udl1_file=values["udl1_file"],
            out_file_path=values.get("out_file_path_1", ""),
        )


def validate_filename(func):
    @functools.wraps(func)
    def wrapper(input_data: InputData):
        if not input_data.udl2_file:
            raise errors.FileError("udl2_file is empty")
        return func(input_data)

    return wrapper


def validate_udl2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            validate_row(args[0])
        else:
            validate_row(kwargs["data"])
        return func(*args, **kwargs)

    return wrapper


def validate_row(data: pd.DataFrame):
    for row in config.udl2_file_keys:
        if row not in data.columns:
            raise errors.FileError(f"file not contain {row}")
