# new const values

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
RISK_ASSESS_VALUE = (
    "高",
    "中",
    "低",
)

POWER_ON_NAME = "通电电位(V_CSE)"
POLAR_NAME = "极化电位(V_CSE)"

# POLAR_NIGHT_20MV = "极化电位正于夜间极化电位+20mV的比例（仅适用于无阴保情况）"
POLAR_NIGHT_20MV = "极化电位相对于自然腐蚀电位正向偏移大于20mV的时间比例"
NIGHT_NAME = "夜间2点到4点极化电位平均值(V_CSE)"
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

__all__ = ["POLAR_NAME_LIST", "AC_DENSITY_VALUE", "AC_DENSITY_VALUE_0_100"]
