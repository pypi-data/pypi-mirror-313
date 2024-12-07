import functools
import typing as t

import pandas as pd

from cp_core.libs.core.filter.errors import EmptyError


def is_empty(df: pd.DataFrame, name: str):
    if df.empty:
        raise EmptyError(f"{name} dataframe is empty.")


def empty_checker(name: str):
    def mywrap(func):
        @functools.wraps(func)  # 需要传入 func 作为参数
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            assert isinstance(df, pd.DataFrame)
            is_empty(df, name)
            return df

        return wrapper

    return mywrap


def postprocess(cleaner):
    """process returned df function with clean"""

    def mywrap(func):
        @functools.wraps
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            return cleaner(df)

        return wrapper

    return mywrap


def pipe_reduce(data, functions):
    return functools.reduce(lambda x, f: f(x), functions, data)
