import functools

# from cp_core.libs.total import types as TOTAL_T
from cp_core.libs.total import controller as total_controller

from .process import FunSetV2

compute = functools.partial(
    total_controller.compute,
    collect_files=functools.partial(
        total_controller.collect_files,
        compute_single=functools.partial(
            total_controller.compute_single, func_set=FunSetV2()
        ),
    ),
)
