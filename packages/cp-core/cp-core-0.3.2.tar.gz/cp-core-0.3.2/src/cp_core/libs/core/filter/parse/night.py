import typing as t
from datetime import datetime, timedelta
from functools import partial

import pandas as pd

from cp_core.libs.core.filter.errors import EmptyError

from ..forms import InputData
from . import const
from .statistic import filter_near, get_night_value


def add_column_data(
    data: pd.DataFrame,
    conf: InputData,
    need: t.List[str],
    names: t.List[str],
):
    # 添加新的列数据
    for label, name in zip(need, names):
        data.insert(0, name, getattr(conf, label))
        data[name] = getattr(conf, label)
    return data


def add_night_data(
    data: pd.DataFrame,
    add_column_data: t.Callable[[pd.DataFrame], pd.DataFrame],
):
    """
    add additional column to data frame.
    The user could ignore add_column_data fn, or implement it by himself
    """
    data = add_column_data(data)
    data = add_night(data)
    return data


def add_night(
    data: pd.DataFrame,
    night_name=const.NIGHT_NAME,
) -> pd.DataFrame:
    """
    check if the data is empty, and add column NIGHT_NAME
    Parameters
    ----------
    data : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    try:
        res = get_night_value(data)
        data[night_name] = res
    except EmptyError:
        data[night_name] = None

    prev = {"value": datetime.now()}
    delta = timedelta(seconds=1)
    f_near = partial(filter_near, prev=prev, delta=delta, keepData=True)

    # 去处多余的一秒数据
    data = data.apply(f_near, axis=1)
    data = data.dropna(subset=[const.DATE_NAME], axis=0, how="any")
    return data
