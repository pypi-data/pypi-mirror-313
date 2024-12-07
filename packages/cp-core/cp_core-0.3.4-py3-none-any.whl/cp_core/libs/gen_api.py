"""functions to generate api"""

import functools

from cp_core.libs import proto
from cp_core.libs.total import controller
from cp_core.libs.total.basic import BasicFuncSet


def get_compute(funcset: BasicFuncSet):
    """隐藏了其他函数的复杂性，直接调用本函数即可完成 compute 函数的生成"""
    return functools.partial(
        controller.compute,
        collect_files=functools.partial(
            controller.collect_files,
            compute_single=functools.partial(
                controller.compute_single,
                func_set=funcset,
            ),
        ),
    )


def get_steps(
    fn: BasicFuncSet,
) -> tuple[proto.UseFilter, proto.UseStat, proto.UseModel]:
    """获取函数集的每一个步骤，可以直接生成新的 api"""

    from cp_core.libs.core.filter.controller import filter_controller
    from cp_core.libs.core.model.controller import model_controller
    from cp_core.libs.core.stat.controller import stat_controller

    def use_filter(params):
        return filter_controller(params, process_data=fn.filter)

    def use_stat(params):
        from cp_core.libs.core.stat.merge import generate_df_from_files

        # 处理多个文件的函数
        f = functools.partial(generate_df_from_files, generate_row=fn.stat)
        return stat_controller(params, process_data=f)

    def use_model(params):
        return model_controller(params, process_data=fn.model)

    return use_filter, use_stat, use_model
