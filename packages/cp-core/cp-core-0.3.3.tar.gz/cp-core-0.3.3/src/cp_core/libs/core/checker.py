"""
file checker
"""

import pandas as pd

from cp_core.libs.core.filter.errors import ColumnError
from cp_core.libs.core.filter.parse.const import (
    CC_AC_READING,
    CC_DC_READING,
    CP_AC_READING,
    CP_DC_READING,
)


def check_cc_and_cp(df: pd.DataFrame):
    check_list = (CP_DC_READING, CP_AC_READING, CC_AC_READING, CC_DC_READING)

    # check if the item of list in columns
    for item in check_list:
        if item not in df.columns:
            raise ColumnError(f"{item} not in columns!")


def check_df_numbers(df: pd.DataFrame):
    if len(df.index) <= 1:
        raise ColumnError("Data items too few.")


def check_col(data: pd.DataFrame, col: str):
    """Check one column in dataframe == empty"""
    assert col in list(data.head())
    data = data[[col]]
    data.dropna(inplace=True)
    assert not data[[col]].empty
