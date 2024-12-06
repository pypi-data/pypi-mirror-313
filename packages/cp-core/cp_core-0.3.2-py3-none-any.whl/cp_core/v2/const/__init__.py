from cp_core.libs.core.filter.parse import const as filter  # noqa

NIGHT_POLAR = "夜间极化电位（V_CSE）"
NIGHT_POWERON = "夜间通电电位（V_CSE）"

POLAR_VALUE = (
    "极化电位正于评判准则的比例/%",
    "极化电位正于评判准则+0.05V的比例/%",
    "极化电位正于评判准则+0.1V的比例/%",
    "极化电位正于评判准则+0.85V的比例/%",
    "极化电位负于评判准则-0.25V的比例/%",
    "极化电位负于评判准则-0.3V的比例/%",
    "极化电位负于评判准则-0.35V的比例/%",
    "极化电位负于评判准则-0.4V的比例/%",
)

JUDGE_METRIC_NAME = "评判准则(V_CSE)"

MODEL_POLAR_VALUE = (
    "断电电位负于-0.9V的比例/%",
    "断电电位在-1.15V~0.9V的比例/%",
)
