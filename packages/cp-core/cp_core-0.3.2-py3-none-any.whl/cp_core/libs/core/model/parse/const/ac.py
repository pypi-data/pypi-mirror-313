from cp_core.libs.core.stat.parse.const import ac

TEST_ID_NAME = ac.TEST_ID_NAME
PIECE_ID_NAME = ac.PIECE_ID_NAME
DATE_NAME = ac.DATE_NAME
PIECE_AREA_NAME = ac.PIECE_AREA_NAME
JUDGE_METRIC = ac.JUDGE_METRIC_NAME

POWERON_NAME = ac.POWER_ON_NAME
POLAR_NAME = ac.POLAR_NAME

AC_DENSE_VALUE = (
    "交流电流密度≥100 A/m^2的比例/%",
    "交流电流密度在30~100 A/m^2的比例/%",
    "交流电流密度<30 A/m^2的比例/%",
)

POLAR_VALUE = (
    "极化电位负于评判准则-0.35V的比例/%",
    "极化电位正于评判准则的比例/%",
)

DC_DENSE_VALUE = ("直流电流密度>1 A/m^2的比例/%",)

RISK_ASSESS_NAME = "风险评判"
RISK_ASSESS_VALUE = (
    "高",
    "中",
    "低",
)
