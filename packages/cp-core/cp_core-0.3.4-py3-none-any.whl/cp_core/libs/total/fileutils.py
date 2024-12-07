# coding: utf-8

import functools
import pathlib
import time
from pathlib import Path

import pandas as pd

from cp_core.config import logger
from cp_core.libs.core.filter.fileutils import read_first_file  # noqa
from cp_core.libs.result import ComputeResult
from cp_core.shared.fileutils import get_output_file_encode

OUTPUT_NAME = "数据模板-第一级"


def merge_files(
    files_xlsx: list[ComputeResult], file_content_list: list[pd.DataFrame]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """files and file content list should be same length"""
    ac_list = []
    dc_list = []
    for f, df in zip(files_xlsx, file_content_list):
        if f.data[-1].current_type == 0:
            ac_list.append(df)
        else:
            dc_list.append(df)

    if len(ac_list) == 0 and len(dc_list) == 0:
        raise ValueError("ac_list 和 dc_list 不能同时为空")

    # 用户不一定需要同时需要 ac 或者 dc 的数据
    if len(ac_list) != 0:
        ac_df = pd.concat(ac_list)
    else:
        ac_df = pd.DataFrame()

    if len(dc_list) != 0:
        dc_df = pd.concat(dc_list)
    else:
        dc_df = pd.DataFrame()

    return ac_df, dc_df


def must_path(func):
    @functools.wraps(func)
    def wrapper(df, udl2_filepath, target_filename):
        """
        如果参数中的 udl2_filepath 的目录不存在，则创建目录; udl2_filepath 也会被强制转换成 Path 类型
        """
        udl2_filepath = Path(udl2_filepath)
        if not udl2_filepath.parent.exists():
            udl2_filepath.parent.mkdir(parents=True, exist_ok=True)
        return func(df, udl2_filepath, target_filename)

    return wrapper


@must_path
def write_file(
    df: pd.DataFrame,
    udl2_filepath: pathlib.Path,
    target_filename: str = "",
):
    """
    将数据写回文件，根据 udl2_filepath 的文件目录进行保存
    :param df: data frame
    :param old_filename: 老文件名，用于提取文件夹，而不是实际的文件名
    :param target_filename: 指定此参数的时候，将使用规范化的文件名
    :return:
    """
    # https://blog.csdn.net/yufengli_/article/details/73699509
    if target_filename == "":
        target_filename = str(
            udl2_filepath.parent / f"{OUTPUT_NAME}-{int(time.time())}.csv"
        )
    else:
        check_target_filename(target_filename)

    logger.info(f"文件 {target_filename} 保存中...")
    writer = df.to_csv(target_filename, encoding=get_output_file_encode(), index=False)
    logger.info(f"{target_filename} 文件保存完成。")
    return writer


def write_to_folder(
    df: pd.DataFrame, output_folder: pathlib.Path, target_filename: str
):
    """
    将数据写入文件夹
    :param df: data frame
    :param output_folder: 输出文件夹
    :param target_filename: 指定的文件名
    :return:
    """

    check_target_filename(target_filename)

    logger.info(f"文件 {target_filename} 保存中...")
    writer = df.to_csv(
        output_folder / target_filename, encoding=get_output_file_encode(), index=False
    )
    logger.info(f"{target_filename} 文件保存完成。")
    return writer


def to_csv(df: pd.DataFrame, target_filename: str):
    assert isinstance(target_filename, str), type(target_filename)
    if target_filename == "":
        raise ValueError("target_filename 不能为空")
    if not target_filename.endswith(".csv"):
        raise ValueError("target_filename 必须以 .csv 结尾")

    pathlib.Path(target_filename).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_filename, encoding=get_output_file_encode(), index=False)


def check_target_filename(target_filename: str):
    if target_filename == "":
        raise ValueError("target_filename 不能为空")

    if Path(target_filename).parent != Path("."):
        raise ValueError("target_filename 不能包含目录")

    if Path(target_filename).suffix != ".csv":
        raise ValueError("target_filename 必须以 .csv 结尾")


def write_excel(df: pd.DataFrame, target_filename: str):
    writer = pd.ExcelWriter(target_filename, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="数据模板")
    writer.close()


def get_file_name(filepath: str) -> str:
    return Path(filepath).name
