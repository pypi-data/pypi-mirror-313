# new const values
DATE_NAME = "Date/Time(中国标准时间)"

DC_CURRENT_NAME = "直流电流(mA)"
DC_CURRENT_DENSITY_NAME = "直流电流密度(A/m^2)"

AC_CURRENT_NAME = "交流电流(mA)"
AC_CURRENT_DENSITY_NAME = "交流电流密度(A/m^2)"

AC_VOL_NAME = "交流电压(V)"
STATUS_NAME = "状态"

AC_DENSITY_VALUE = (
    "交流电流密度>300 A/m2的比例/%",
    "交流电流密度≥100 A/m^2的比例/%",
    "交流电流密度在30~100 A/m^2的比例/%",
    "交流电流密度<30 A/m^2的比例/%",
)

TEST_ID_NAME = "测试桩编号"
PIECE_ID_NAME = "试片编号"
PIECE_AREA_NAME = "试片面积(cm^2)"
RISK_ASSESS_NAME = "风险评判"

RISK_ASSESS_VALUE_V3 = (
    "高",
    "中",
    "低",
    "数据缺失",
)

POWER_ON_NAME = "通电电位(V_CSE)"
POLAR_NAME = "极化电位(V_CSE)"
DC_DENSITY_NAME = "直流电流密度(A/m^2)"

# POLAR_NIGHT_20MV = "极化电位正于夜间极化电位+20mV的比例（仅适用于无阴保情况）"
POLAR_NIGHT_20MV = "极化电位相对于自然腐蚀电位正向偏移大于20mV的时间比例"
POLAR_005_03 = "负于最小保护准则-0.05V到正于最小保护准则-0.3V的比例"

JUDGE_METRIC_NAME = "评判准则(V_CSE)"

POLAR_NAME_LIST: list[str] = [
    "正于评判准则比例",
    "正于评判准则+0.05V比例",
    "正于评判准则+0.1V比例",
    "正于评判准则+0.85V比例",
    "小于评判准则-0.3V比例",
    "小于评判准则-0.05V比例",
    "小于评判准则-0.25V比例",
    "小于评判准则-0.3V比例",
    "小于评判准则-0.35V比例",
    "小于评判准则-0.4V比例",
    POLAR_005_03,
    POLAR_NIGHT_20MV,
]

POLAR_VALUE_WITHOUT_PROTECT = ("正于评判准则+20mV比例/%",)

AC_DENSITY_VALUE_0_100 = "交流电流密度在0~100A/m^2的比例/%"

AC_VOL_VALUE = (
    "交流电压>15 V的比例/%",
    "交流电压>10 V的比例/%",
    "交流电压>4 V的比例/%",
)

__all__ = [
    "POLAR_NAME_LIST",
    "AC_DENSITY_VALUE",
    "AC_DENSITY_VALUE_0_100",
    "AC_VOL_VALUE",
]

NIGHT_POWERON = "夜间通电电位(V_CSE)"
NIGHT_POLAR_AVG = "夜间极化电位(V_CSE)平均值"
NIGHT_NAME = NIGHT_POLAR_AVG
NIGHT_NAME_OLD = "夜间2点到4点极化电位平均值(V_CSE)"

# v1
DENSITY_VALUE_v1 = (
    "直流电流密度>1A/m^2的平均值",
    "直流电流密度>0.1A/m^2的平均值",
    "直流电流密度>0A/m^2的平均值",
    "直流电流密度<0A/m^2的平均值",
    "直流电流密度<-0.1A/m^2的平均值",
    "直流电流密度<-1A/m^2的平均值",
)
