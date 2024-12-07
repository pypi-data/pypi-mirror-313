"""
handle windows event
"""

import functools
import typing as t

import pandas as pd

from cp_core.config import logger
from cp_core.exception import ValidateError
from cp_core.libs import types as T
from cp_core.libs.core.filter import extract
from cp_core.libs.result import Result, Status

from . import errors, fileutils, forms
from .errors import FileError


def _transform(values: T.FilterParams):
    """
    transform area and resistivity value to normal format
    :param values:
    :return:
    """
    try:
        values["piece_area"] = float(values["piece_area"])
        values["resistivity"] = float(values["resistivity"])
    except TypeError as e:
        logger.error(e)
        raise e
    except ValueError as e:
        logger.error(e)
        raise e
    return values


def validate_config(
    values: T.FilterParams,
) -> forms.InputData:
    input_data = forms.InputData.model_validate(values)
    return input_data


@forms.validate_filename
def process_data(input_data: forms.InputData) -> pd.DataFrame:
    """
    filter the origin data.
    """

    # 读取不同的文件
    data = fileutils.read_first_file(input_data.udl2_file)
    f2_name = input_data.udl1_file

    # 如果 udl1 文件存在，那么需要获取一下 udl1 文件的类型
    if f2_name:
        types = fileutils.get_file_type(f2_name)
    else:
        types = "none"

    # 只需要处理 udl2 的话
    if not f2_name:
        res_data = extract.extract_data_from_udl2(data, input_data)
    else:
        data2 = fileutils.read_second_file(f2_name)
        res_data = extract.extract_data_from_udl1(
            types, udl2_data=data, second_data=data2, params=input_data
        )
    return res_data


def validate(func):
    @functools.wraps(func)
    def wrapper(values: T.FilterParams):
        try:
            validate_config(values)
        except ValidateError as e:
            logger.error(e)
            return Result(status=Status.failed, msg=str(e))
        return func(values)

    return wrapper


def transform_values(func):
    """This function fix some value in dict"""

    @functools.wraps(func)
    def wrapper(values: T.FilterParams, *args, **kwargs):
        values = _transform(values)
        return func(values, *args, **kwargs)

    return wrapper


class FilterData(t.Protocol):
    def __call__(self, params: forms.InputData) -> pd.DataFrame: ...


@transform_values
def filter_controller(
    values: T.FilterParams,
    process_data: FilterData = process_data,
) -> Result:
    """
    confirm event for first application [filter]
    :param values:
    :return:
    """

    # 检查配置
    try:
        # transfer values to normal type. change the values in function
        res = validate_config(values)
    except ValidateError as e:
        logger.error(e)
        return Result(status=Status.failed, msg=str(e))

    logger.info("final: ", values)
    logger.info("start process data...")

    try:
        # 处理数据
        df = process_data(res)
        fileutils.to_csv(df, values.get("out_file_path", ""))
    except (FileError, errors.FilterError) as e:
        # 处理 Excel 问题, Filter 的问题
        return Result(status=Status.failed, msg=str(e))

    return Result(status=Status.success, msg="success")
