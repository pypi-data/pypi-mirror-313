import pandas as pd


def check_col(data: pd.DataFrame, col: str):
    """Check one column in dataframe == empty"""
    assert col in list(data.head())
    data = data[[col]]
    data.dropna(inplace=True)
    assert not data[[col]].empty
