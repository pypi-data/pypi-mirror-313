import pandas as pd

from .parse.const import ac, dc


def get_data_value(data: pd.DataFrame, name: str):
    return data[[name]].values[0]


def judge_risk_ac(data: pd.DataFrame) -> str:
    high, mid, low = ac.RISK_ASSESS_VALUE

    if data[ac.AC_DENSE_VALUE[0]].values[0] > 0:
        return high

    if data[ac.AC_DENSE_VALUE[1]].values[0] > 0:
        if data[ac.POLAR_VALUE[0]].values[0] > 20:
            return high
        if data[ac.DC_DENSE_VALUE[0]].values[0] > 20:
            return high

    if data[ac.POLAR_VALUE[1]].values[0] > 20:
        return high

    if data[ac.AC_DENSE_VALUE[2]].values[0] == 100:
        return low

    return mid


def judge_risk_dc(data: pd.DataFrame, yinbao: bool):
    high, mid, low = dc.RISK_ASSESS_VALUE
    if yinbao:
        if get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[0]) <= 5:
            if get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[1]) <= 20:
                if get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[2]) <= 1:
                    return low

        if get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[0]) > 20:
            return high

        if get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[1]) > 15:
            return high

        if get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[2]) > 5:
            return high

        if 0.05 < get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[0]) <= 15:
            if 0.02 < get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[1]) <= 15:
                if 0.01 < get_data_value(data, dc.POLAR_VALUE_WITH_PROTECT[2]) <= 5:
                    return mid
    else:
        if get_data_value(data, dc.POLAR_VALUE_WITHOUT_PROTECT[0]) <= 5:
            return low
        elif 5 < get_data_value(data, dc.POLAR_VALUE_WITHOUT_PROTECT[0]) <= 15:
            return mid
        else:
            return high

    return mid
