# coding: utf-8

from __future__ import annotations

import os

from pydantic import BaseModel, Field

from cp_core.exception import FileError
from cp_core.libs.comprehensive.validate import parse_external


def judge_file(filename: str):
    if not os.path.exists(filename):
        raise FileError(f"File: {filename} is not exist.")
    if not (
        filename.endswith("csv")
        or filename.endswith("xls")
        or filename.endswith("xlsx")
    ):
        raise FileError(f"File: {filename} is not endswith csv/els/xlsx")


def judge_file_inner(filename: str):
    """
    judge the inner content in file.
    :param filename:
    :return:
    """
    pass


class Sumer(BaseModel):
    types: int = Field(..., ge=0, le=1)
    is_protect: int = Field(..., ge=0, le=1)
    file_path: str
    out_file_path: str


def parse_sumer(values: dict) -> dict:
    data = Sumer.model_validate(values)
    judge_file(filename=data.file_path)
    return data.model_dump()


class Filter(BaseModel):
    device_id: str
    resistivity: float
    piece_id: str
    piece_area: float
    file_path: str
    out_file_path: str


def validate_filter(values: dict) -> dict:
    data = Filter.model_validate(values)
    judge_file(filename=data.file_path)
    return data.model_dump()


class Total(BaseModel):
    types: int
    is_protect: int
    device_id: str
    piece_id: str
    piece_area: float
    resistivity: float
    judge_metric: float
    udl2_file: str
    udl1_file: str | None
    out_file_path_1: str
    out_file_path_2: str
    out_file_path_3: str


class ModalParams(BaseModel):
    types: int = Field(..., ge=0, le=1)
    is_protect: int = Field(..., ge=0, le=1)
    resistivity: float
    judge_metric: float
    file_path: str
    out_file_path: str


class ValidateUtils:
    """
    TODO[svtter]: need to remove class.

    class is not good for python patterns because of refactor method.
    good for read
    """

    @classmethod
    def total(cls, values: dict):
        data = Total.model_validate(values)
        judge_file(filename=data.udl2_file)

        if data.udl1_file:
            judge_file(filename=data.udl1_file)
        return data.model_dump()

    @classmethod
    def model(cls, values: dict):
        data = ModalParams.model_validate(values)
        judge_file(filename=data.file_path)
        return data.model_dump()


class Config(BaseModel):
    period: int = Field(..., ge=1, le=5)


def parse_config(values: dict) -> dict:
    data = Config.model_validate(values)
    period = data.period

    # different period to function
    parser = {
        1: validate_filter,
        2: parse_sumer,
        3: ValidateUtils.model,
        4: ValidateUtils.total,
        5: parse_external,
    }

    res = parser[period](values)
    return res
