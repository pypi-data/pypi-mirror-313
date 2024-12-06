""" """

import pandas as pd

from . import const


def compare_interference_vol(
    udl2_data: pd.DataFrame, udl1_data: pd.DataFrame
) -> pd.Series:
    """
    Choose the potential_ac_reading
    Parameters
    ----------
    udl2_data :
    udl1_data :

    Returns
    -------

    """

    if udl2_data[const.AC_VOL_NAME].mean() > udl1_data[const.AC_VOL_NAME].mean():
        return udl2_data[const.AC_VOL_NAME]
    else:
        return udl1_data[const.AC_VOL_NAME]
