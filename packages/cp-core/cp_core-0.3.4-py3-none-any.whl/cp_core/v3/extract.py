import typing as t

import pandas as pd

# 使用原本的extract_data_from_udl2
from cp_core.libs.core.filter.extract import extract_data_from_udl2  # noqa
from cp_core.libs.core.filter.parse import date

from . import night


def obtain_night_data(df: pd.DataFrame) -> pd.DataFrame:
    df, _ = date.str2datetime_first_time(df)
    poweron_data = night.extract_night_poweron_data(df)
    # polar_avg = night.extract_night_polar_avg(df)
    return poweron_data
