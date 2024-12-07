import typing as t

import pandas as pd


def run_pipe(init_df: pd.DataFrame, pipeline: list[t.Callable]):
    """运行 pipeline 中所有的函数，依次运行"""
    df = init_df.copy()
    for fn in pipeline:
        df = fn(df)
    return df
