# coding: utf-8

import sys
import unittest

from cp_core.libs.core.stat.parse.ac_value import (
    ac_density,
    ac_voltage,
    dc_density,
    polar,
)
from cp_core.libs.core.stat.parse.const.ac import (
    AC_DENSITY_NAME,
    AC_VOL_NAME,
    DC_DENSITY_NAME,
    POLAR_NAME,
)


def test_polarization(get_data):
    # data
    data = get_data
    se = data[[POLAR_NAME]]
    se.dropna(inplace=True)
    metrics = -0.85
    res = polar(se, metrics)
    print(res, file=sys.stderr)


def test_dc_density(get_data):
    data = get_data
    se = data[[DC_DENSITY_NAME]]
    se.dropna(inplace=True)
    res = dc_density(se)
    print(res)


def test_ac_voltage(get_data):
    data = get_data
    se = data[[AC_VOL_NAME]]
    se.dropna(inplace=True)
    res = ac_voltage(se)
    print(res)


def test_ac_density(get_data):
    data = get_data
    se = data[[AC_DENSITY_NAME]]
    se.dropna(inplace=True)
    res = ac_density(se)
    print(res)
