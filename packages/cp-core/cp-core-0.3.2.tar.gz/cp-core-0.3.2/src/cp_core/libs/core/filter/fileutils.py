"""
process excel
"""

import os
import time
from pathlib import Path

import pandas as pd

from cp_core.config import logger
from cp_core.libs.core.filter.errors import FileError
from cp_core.shared.fileutils import get_output_file_encode, to_csv  # noqa
from cp_core.utils import read_csv

from .msg import OUTPUT_NAME


def file_name_check(file_path: str, types: str):
    path = Path(file_path)
    suffix = Path(file_path).suffix

    if not os.path.exists(path):
        raise FileError(FileError.not_found + f"path: {path}")

    if types == "udl2":
        if path.name.find("udl2") < 0:
            raise FileError(FileError.not_found_udl2)
        if suffix != ".csv":
            raise FileError(FileError.not_csv)

    elif types == "udl1 or Anko":
        if path.name.find("udl1") == -1 and path.name.find("Anko") == -1:
            raise FileError(FileError.not_found_anko_and_udl1)
    else:
        raise FileError("File type not support")


def get_file_type(file_path: str) -> str:
    """
    获取第二个文件的类型
    :param file_path:
    :return:
    """
    file_types = ("udl1", "Anko")
    for types in file_types:
        if file_path.find(types) != -1:
            return types
    raise FileError(f"not such filetype: {file_path}")


def read_first_file(path: str) -> pd.DataFrame:
    """
    read data from path and handle it
    :param path:
    :return:
    """
    try:
        file_name_check(path, types="udl2")
        data = read_csv(path)
        return data
    except FileError as e:
        logger.error(e)
        raise e


def read_second_file(path: str) -> pd.DataFrame:
    types = get_file_type(path)
    if types == "udl1":
        data = read_csv(path)
    elif types == "Anko":
        data = open_anko_file(path)
    else:
        # 抛出 FileError
        raise FileError(FileError.not_support)
    return data


def write_file(df, old_filename: str, target_filename: str = ""):
    """
    将数据写回文件
    :param df: data frame
    :param old_filename: 老文件名
    :param target_filename: 指定此参数的时候，
    :return:
    """
    # https://blog.csdn.net/yufengli_/article/details/73699509
    logger.info(f"文件{target_filename}保存中...")
    if target_filename == "":
        path = Path(old_filename)
        target_filename = str(
            path.parent / f"{OUTPUT_NAME}-{path.parts[-1]}-{int(time.time())}.csv"
        )
    # writer.save()
    writer = df.to_csv(target_filename, encoding=get_output_file_encode(), index=False)
    if not os.path.exists(target_filename):
        raise FileError(f"保存失败, filepath: {target_filename}")
    logger.info(f"文件{target_filename}保存完成。")
    return writer


def open_anko_file(filename):
    """
    transfer old anko file to normal format and open it.
    """
    path = Path(filename)
    parent = path.parent

    with open(filename, encoding="gbk") as f:
        line = f.readline()
        while line != None:
            if line.startswith("Index"):
                content = f.readlines()
                break
            line = f.readline()

    content = [line, *content]
    name = int(time.time())
    filename = f"{parent}/temp-{name}.csv"
    with open(filename, "w", encoding="gbk") as f:
        f.writelines(content)

    data = read_csv(filename)

    # remove the temp file
    os.remove(filename)
    return data
