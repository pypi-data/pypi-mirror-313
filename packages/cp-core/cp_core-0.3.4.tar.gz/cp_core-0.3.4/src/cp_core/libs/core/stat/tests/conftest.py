import os

import pytest

from cp_core.config import project_root
from cp_core.libs.core.stat.file import load_file
from cp_core.tests.path import csv_folder

# FILE_PATH = '/Users/xiuhao/work/data/material/给修昊10.23/交流模块/交流数据模板V3.xlsx'


@pytest.fixture
def FILE_PATH():
    return os.path.join(project_root, csv_folder, "data/stat/jiaoliu.xlsx")


@pytest.fixture
def get_data(FILE_PATH):
    return load_file(FILE_PATH)
