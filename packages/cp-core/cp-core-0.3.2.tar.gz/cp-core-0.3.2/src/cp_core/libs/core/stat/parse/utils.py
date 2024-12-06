import datetime

import numpy as np
import pandas as pd

from .const import ac as const_ac


def transform_date(data: pd.Series):
    if isinstance(data[const_ac.DATE_NAME], datetime.datetime):
        date = data[const_ac.DATE_NAME]
    elif isinstance(data[const_ac.DATE_NAME], str):
        date = pd.to_datetime(data[const_ac.DATE_NAME])
    elif isinstance(data[const_ac.DATE_NAME], pd.Timestamp):
        date = data[const_ac.DATE_NAME]
    elif isinstance(data[const_ac.DATE_NAME], np.int64):
        date = pd.Timestamp(data[const_ac.DATE_NAME])
    else:
        date = data[const_ac.DATE_NAME].to_pydatetime()

    return date
