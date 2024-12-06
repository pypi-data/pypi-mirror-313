import datetime

import pandas as pd

from cp_core.v3 import night
from cp_core.v3.config import RESOURCE_FOLDER
from cp_core.v3.night import const, statistic


def test_filter_relay_name():
    df = pd.read_csv(RESOURCE_FOLDER / "v3/filter/night_pDC_off_relay.csv")
    df[const.DATE_NAME] = pd.to_datetime(df[const.DATE_NAME])
    res = night.filter_relay_name(df, 1)
    assert not res.empty
    assert len(res) == 10


def test_poweron_data():
    df = pd.read_csv(RESOURCE_FOLDER / "v3/filter/night_pDC.csv")
    df[const.DATE_NAME] = pd.to_datetime(df[const.DATE_NAME])

    res = night.extract_night_poweron_data(df)
    # res.to_csv("./tmp/test_night_pDC.csv")
    assert not res.empty, "night_pDC.csv contains no data."
    assert res.columns.tolist() == [const.DATE_NAME, const.NIGHT_POWERON]


def test_polar_night_avg():
    # 读取测试数据
    df = pd.read_csv(RESOURCE_FOLDER / "v3/filter/night_pDC_off.csv")
    df[const.DATE_NAME] = pd.to_datetime(df[const.DATE_NAME])

    res = night.extract_night_polar_avg(df)

    # res.to_csv("./tmp/test_night_pDC_off.csv")
    assert not res.empty, "night_pDC_off.csv contains no data."
    assert res.columns.tolist() == [
        const.DATE_NAME,
        const.NIGHT_POLAR_AVG,
    ]


def test_extract_night_data():
    """测试 extract_night_data 是否工作"""
    # 读取测试数据
    df = pd.read_csv(RESOURCE_FOLDER / "v3/filter/night.csv")
    df[const.DATE_NAME] = pd.to_datetime(df[const.DATE_NAME])

    res = night.extract_night_data(df)
    assert not res.empty, "night.csv contains 2:00am data."
    assert res.columns.tolist() == [
        "Date/Time(中国标准时间)",
        const.NIGHT_POWERON,
    ]


def test_filter_time():
    """测试 filter time 的内容"""
    dt = pd.to_datetime("2024-01-01 01:01:00")
    test_cases = (
        (
            pd.DataFrame(
                {
                    const.DATE_NAME: [dt],
                    const.pDC: [100],
                }
            ),
            True,
        ),
        (
            pd.DataFrame(
                {
                    const.DATE_NAME: [dt + datetime.timedelta(hours=1)],
                    const.pDC: [100],
                }
            ),
            False,
        ),
    )

    for df, expected in test_cases:
        res = df.apply(lambda x: statistic.filter_time(x, const.pDC), axis=1)
        res.dropna(inplace=True)
        assert res.empty == expected


def get_df(filename: str):
    df = pd.read_csv(RESOURCE_FOLDER / "v3/filter/merge" / filename)
    df[const.DATE_NAME] = pd.to_datetime(df[const.DATE_NAME])
    return df


def test_merge_night_data():
    poweron_data = night.extract_night_poweron_data(get_df("night_pDC.csv"))
    polar_avg = night.extract_night_polar_avg(get_df("night_pDC_off.csv"))
    res = night.merge_night_data(poweron_data, polar_avg)
    # res.to_csv("./tmp/night_merge.csv", index=False)
    assert not res.empty
