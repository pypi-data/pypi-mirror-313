# coding: utf-8
# author: svtter
# time:
""" """

from __future__ import annotations

import time
import typing as t
from pathlib import Path

import pandas as pd

from cp_core.config import logger
from cp_core.libs import types as T
from cp_core.shared.judge import is_protect, is_zhiliu


def get_filtered_file(values: T.StatParams) -> tuple[str, ...]:
    files = values["filtered_file"]
    res = files.split(";")
    return tuple(res)


def load_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".xlsx"):
        data = pd.read_excel(file_path)
    else:
        try:
            data = pd.read_csv(file_path)
        except UnicodeDecodeError:
            data = pd.read_csv(file_path, encoding="gbk")
    return data


def gen_output_name(values: dict):
    output_name = {
        "jiaoliu": "交流统计数据-第二级",
        "zhiliu-protect": "直流统计数据-有阴保-第二级",
        "zhiliu-no-protect": "直流统计数据-无阴保-第二级",
    }

    if is_zhiliu(values) and is_protect(values):
        return output_name["zhiliu-protect"]
    if is_zhiliu(values) and not is_protect(values):
        return output_name["zhiliu-no-protect"]
    if not is_zhiliu(values):
        return output_name["jiaoliu"]


def write_file(
    df, old_filename: str, target_filename: str = "", values: dict | t.Any = {}
):
    """
    将数据写回文件
    :param df: data frame
    :param old_filename: 老文件名
    :param target_filename: 指定此参数的时候，
    :param values: 参数
    :return:
    """
    # https://blog.csdn.net/yufengli_/article/details/73699509
    logger.info(f"文件{target_filename}保存中...")
    if target_filename == "":
        path = Path(old_filename)
        OUTPUT_NAME = gen_output_name(values)
        # target_filename = path.parent / f'{OUTPUT_NAME}-{int(time.time())}.xlsx'
        origin_name = path.parts[-1][9:-4]
        target_filename = str(
            path.parent / f"{OUTPUT_NAME}-{origin_name}-{int(time.time())}.csv"
        )

    # writer = pd.ExcelWriter(target_filename)
    # df.to_excel(writer, index=False, encoding='gbk', sheet_name='数据模板')
    # writer.save()
    writer = df.to_csv(target_filename, encoding="gbk", index=False)
    logger.info(f"文件{target_filename}保存完成。")
    return writer
