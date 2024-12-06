# coding: utf-8
# author: svtter
# time:
"""
所有表格中的固定名称

"""

DATE_NAME = "Date/Time(中国标准时间)"
RESISTIVITY_NAME = "土壤电阻率(Ω*m)"
TEST_ID_NAME = "测试桩编号"
PIECE_ID_NAME = "试片编号"
PIECE_AREA_NAME = "试片面积(cm^2)"

JUDGE_METRIC_NAME = "评判准则(V_CSE)"
POWER_ON_NAME = "通电电位(V_CSE)"
POLAR_NAME = "极化电位(V_CSE)"
DC_DENSITY_NAME = "直流电流密度(A/m^2)"
AC_VOL_NAME = "交流电压(V)"
AC_DENSITY_NAME = "交流电流密度(A/m^2)"
NIGHT_NAME = "夜间2点到4点极化电位平均值(V_CSE)"


POLAR_VALUE = (
    "极化电位正于评判准则的比例/%",
    "极化电位正于评判准则+0.05V的比例/%",
    "极化电位正于评判准则+0.1V的比例/%",
    "极化电位正于评判准则+0.85V的比例/%",
    "极化电位负于评判准则-0.1的比例/%",
    "极化电位负于评判准则-0.2V的比例/%",
    "极化电位负于评判准则-0.35V的比例/%",
)

DC_DENSITY_VALUE = (
    "直流电流密度>1 A/m^2的比例/%",
    "直流电流密度>0.1 A/m^2的比例/%",
    "直流电流密度>0 A/m^2的比例/%",
    "直流电流密度<0 A/m^2的比例/%",
    "直流电流密度<-0.1 A/m^2的比例/%",
    "直流电流密度<-1 A/m^2的比例/%",
)

AC_VOL_VALUE = (
    "交流电压>15 V的比例/%",
    "交流电压>10 V的比例/%",
    "交流电压>4 V的比例/%",
)

AC_DENSITY_VALUE = (
    "交流电流密度>300 A/m2的比例/%",
    "交流电流密度≥100 A/m^2的比例/%",
    "交流电流密度在30~100 A/m^2的比例/%",
    "交流电流密度<30 A/m^2的比例/%",
)
