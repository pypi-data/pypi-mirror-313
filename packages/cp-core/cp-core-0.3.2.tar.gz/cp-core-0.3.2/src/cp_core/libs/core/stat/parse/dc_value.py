# coding: utf-8
# author: svtter
# time: ...

""" """

from __future__ import annotations

import datetime
import functools
import typing as t

import pandas as pd

from .const import ac as const_ac
from .dc_percent import polarization as polar_percent
from .utils import transform_date
from .value import get_max_min_average, poweron


def _filter_time_between_2am_to_4am(data: pd.Series, types: str) -> pd.Series:
    """
    filter 2am - 4pm data
    """
    # use new api: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.between_time.html
    date = transform_date(data)
    data[const_ac.DATE_NAME] = date

    if 2 <= date.hour <= 4:
        return data
    else:
        name = const_ac.POWER_ON_NAME if types == "poweron" else const_ac.POLAR_NAME
        data[name] = None
        return data


def _filter_diff_date(data: pd.DataFrame):
    same = {
        "day": None,
        "value": True,
    }

    def check_date(se: pd.Series, s: dict):
        if not s.get("value"):
            return

        temp = se[const_ac.DATE_NAME]
        if not s.get("day"):
            s["day"] = temp.day
        if s.get("day") == temp.day:
            return
        else:
            s["date"] = temp.day
            s["value"] = False

    # find if there are two days
    check_func = functools.partial(check_date, s=same)
    data.apply(check_func, axis=1)

    # there's no second day
    if same.get("value"):
        return data

    def filter_date(se: pd.Series, day):
        if se[const_ac.DATE_NAME].day != day:
            return None
        else:
            return se

    filter_func = functools.partial(filter_date, day=same.get("day"))
    data = data.apply(filter_func, axis=1)

    return data


def _filter_data(data: pd.DataFrame, types: str) -> pd.DataFrame:
    """
    过滤数据
    """
    assert types in ("poweron", "polar")
    filter_power_on = functools.partial(_filter_time_between_2am_to_4am, types=types)
    df = data.apply(filter_power_on, axis=1)

    name = const_ac.POWER_ON_NAME if types == "poweron" else const_ac.POLAR_NAME
    df = df[[const_ac.DATE_NAME, name]]
    df.dropna(inplace=True)
    df = _filter_diff_date(df)
    return df


def get_night_value(data: pd.DataFrame, types: str, need_filter: bool = True) -> list:
    """
    获取夜间数据
    """
    if need_filter:
        df = _filter_data(data, types)
    else:
        df = data
    name = const_ac.POWER_ON_NAME if types == "poweron" else const_ac.POLAR_NAME
    result_list = get_max_min_average(name, data=df)
    result_list = [("夜间" + name, val) for name, val in result_list]
    return result_list


def polar(
    data: pd.DataFrame,
    is_protect: bool,
    interval_jihua: bool,
    get_metric: t.Callable,
    polar_percent_func=polar_percent,
) -> list[tuple[str, t.Any]]:
    df = data[[const_ac.POLAR_NAME]]
    if interval_jihua:
        df[const_ac.POLAR_NAME] = df[const_ac.POLAR_NAME][::2]

    metric = get_metric()

    res = [
        *get_max_min_average(const_ac.POLAR_NAME, df),
        *polar_percent_func(df[const_ac.POLAR_NAME], metric, is_protect),
    ]
    return res


def density(data: pd.DataFrame):
    from .dc_percent import density as get_percent
    from .dc_percent import filter_density as get_value

    res = [
        *get_max_min_average(const_ac.DC_DENSITY_NAME, data),
        *get_value(data[const_ac.DC_DENSITY_NAME]),
        *get_percent(data[const_ac.DC_DENSITY_NAME]),
    ]
    return res


def ac_vol(data: pd.DataFrame):
    return get_max_min_average(const_ac.AC_VOL_NAME, data)


def ac_density(data: pd.DataFrame):
    return get_max_min_average(const_ac.AC_DENSITY_NAME, data)


def convert_datetime(func):
    @functools.wraps(func)
    def wrapper(data: pd.DataFrame, *args, **kwargs):
        if not isinstance(data[const_ac.DATE_NAME].values[0], datetime.datetime):
            # data[DATE_NAME] = data[DATE_NAME].apply(to_datetime)
            data[const_ac.DATE_NAME] = pd.to_datetime(data[const_ac.DATE_NAME])
        return func(data, *args, **kwargs)

    return wrapper


@convert_datetime
def get_all(
    data: pd.DataFrame,
    judge_metrics: float,
    values: dict,
    interval_jihua: bool,
) -> list:
    def get_metric():
        return judge_metrics

    res = [
        *get_night_value(data, types="poweron"),
        *get_night_value(data, types="polar"),
        (const_ac.JUDGE_METRIC_NAME, judge_metrics),
        *poweron(data),
        *polar(
            data,
            values["is_protect"],
            interval_jihua=interval_jihua,
            get_metric=get_metric,
        ),
        *density(data),
        *ac_vol(data),
        *ac_density(data),
    ]

    return res
