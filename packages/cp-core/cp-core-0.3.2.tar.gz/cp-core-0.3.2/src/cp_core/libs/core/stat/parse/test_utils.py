import pandas as pd

from . import utils


def test_transform_date():
    data = pd.Series(index=["Date/Time(中国标准时间)"], data=[10123456789])
    date = utils.transform_date(data)
    assert isinstance(date, pd.Timestamp)
