import pathlib

import pandas as pd
import pytest

from cp_core.v3.config import RESOURCE_FOLDER
from tests.v3_test.udl2_inputdata import values


@pytest.fixture
def udl2_data() -> pd.DataFrame:
    return pd.read_csv(
        RESOURCE_FOLDER / "v3/real/AF031 udl2_sn023293.csv",
        encoding="gbk",
    )


@pytest.fixture
def stage_1_result() -> pd.DataFrame:
    return pd.read_csv(RESOURCE_FOLDER / "v3/real/stage-1-result.csv")


@pytest.fixture
def stage_2_result(is_zhiliu: int, is_protect: int):
    return pd.read_csv(
        f"./tmp/stage-2-result-{'ac' if is_zhiliu == 0 else 'dc'}-protect-{is_protect}.csv"
    )


@pytest.fixture
def avg_data() -> pd.DataFrame:
    return pd.read_csv(RESOURCE_FOLDER / "v3/stat/test_avg_data.csv")


@pytest.fixture
def tmp_folder() -> pathlib.Path:
    return pathlib.Path("./tmp")


@pytest.fixture
def get_df() -> pd.DataFrame:
    return pd.read_csv(values.udl2_file, encoding="gbk")
