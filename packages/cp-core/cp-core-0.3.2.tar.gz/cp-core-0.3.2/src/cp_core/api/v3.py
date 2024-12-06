"""
controller 是处理请求的基本单位。
"""

from cp_core.libs.gen_api import get_compute, get_steps
from cp_core.v3.funcset import FuncSetV3

fn = FuncSetV3()
compute = get_compute(fn)
use_filter, use_stat, use_model = get_steps(fn)
