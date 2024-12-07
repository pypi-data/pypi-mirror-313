import typing as t

import pandas as pd


def to_df(df_list: list[list[tuple[str, t.Any]]]) -> pd.DataFrame:
    """将嵌套的列表转换为DataFrame"""
    data = (dict(iter(row)) for row in df_list)
    df = pd.DataFrame(data)
    return df
