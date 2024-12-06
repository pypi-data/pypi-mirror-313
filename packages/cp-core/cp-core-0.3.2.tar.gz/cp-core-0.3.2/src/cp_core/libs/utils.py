import typing as t

import pandas as pd


def get_debug() -> bool:
    import ast
    import os

    return ast.literal_eval(os.getenv("DEBUG", "False"))


def to_csv_fn(get_d_fn: t.Callable[[], pd.DataFrame], start: int = 0):
    """快速将 csv 写入数据"""

    i = start

    def fn(filename=""):
        nonlocal i
        if filename == "":
            filename = f"data-{i}.csv"
        d = get_d_fn()
        d.to_csv(filename)
        i += 1

    return fn
