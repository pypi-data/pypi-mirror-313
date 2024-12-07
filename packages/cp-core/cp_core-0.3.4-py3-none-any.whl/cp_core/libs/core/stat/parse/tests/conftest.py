# coding: utf-8
# author: svtter
# time:
""" """

import pandas as pd
import pytest

from cp_core.libs.core.stat.file import load_file
from cp_core.tests.path import csv_folder


@pytest.fixture
def get_data():
    # return load_file('/Users/xiuhao/work/data/material/给修昊10.23/交流模块/交流数据模板V3.xlsx')
    # filename = r'C:\Users\Administrator\Documents\work\项目\给修昊10.23\交流模块\交流数据模板V3.xlsx'
    filename = f"{csv_folder}/data/stat/jiaoliu.xlsx"
    return load_file(filename)


@pytest.fixture
def get_data_sheet():
    # fname = r'C:\Users\Administrator\Documents\work\项目\给修昊10.23\直流模块\直流数据模板-调试结果数据(无阴保).xlsx'
    fname = f"{csv_folder}/data/stat/zhiliu-no-protect.xlsx"
    data = pd.read_excel(fname)
    return data
