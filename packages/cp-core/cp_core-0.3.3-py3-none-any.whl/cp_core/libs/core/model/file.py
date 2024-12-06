# coding: utf-8
# author: svtter
# time:
""" """

import time
from pathlib import Path

import pandas as pd

from cp_core.config import logger
from cp_core.libs import types as T
from cp_core.libs.core.stat.merge import is_zhiliu
from cp_core.shared.judge import is_protect
from cp_core.utils import read_csv


def load_file(filename: str) -> pd.DataFrame:
    if filename.endswith("xlsx"):
        data = pd.read_excel(filename)
    else:
        data = read_csv(filename)
    return data


def gen_output_name(values):
    output_name = {
        "jiaoliu": "交流干扰风险评价-第三级",
        "zhiliu-no-protect": "直流干扰风险评价-无阴保-第三级",
        "zhiliu-protect": "直流干扰风险评价-有阴保-第三级",
    }
    if is_zhiliu(values) and is_protect(values):
        return output_name["zhiliu-protect"]
    if is_zhiliu(values) and not is_protect(values):
        return output_name["zhiliu-no-protect"]
    if not is_zhiliu(values):
        return output_name["jiaoliu"]


def write_file(df, old_filename: str, values: T.ModelParams, target_filename: str = ""):
    """
    将数据写回文件
    :param df: data frame
    :param old_filename: 老文件名
    :param target_filename: 指定此参数的时候，
    :param values: 配置
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

    # use csv instead.
    writer = df.to_csv(target_filename, encoding="gbk", index=False)
    logger.info(f"文件{target_filename}保存完成。")
    return writer
