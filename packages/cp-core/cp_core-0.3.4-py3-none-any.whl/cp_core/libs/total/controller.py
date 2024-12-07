import typing as t

import pandas as pd

from cp_core.libs import result
from cp_core.libs.core.filter.controller import (
    process_data as filter_process,
)
from cp_core.libs.core.filter.forms import InputData
from cp_core.libs.core.model.controller import (
    handle_ac_dc_data as model_process,
)
from cp_core.libs.core.stat.merge import (
    generate_row_from_data as stat_process,
)
from cp_core.libs.types import ModelParams, Params, StatParams
from cp_core.shared.judge import is_zhiliu

from . import fileutils
from . import types as T
from .basic import BasicFuncSet
from .validate import validate


class FuncSet(BasicFuncSet):
    """sets of three step functions"""

    def filter(self, input_data: InputData):
        return filter_process(input_data)

    def stat(self, df: pd.DataFrame, params: StatParams | Params, interval_jihua: bool):
        return stat_process(df, params, interval_jihua)

    def model(self, df: pd.DataFrame, params: ModelParams):
        return model_process(df, params)


def use_write_data(
    id: int,
    original: str,
    append: t.Callable,
    current_type: int,
) -> t.Callable:
    """返回一个写入数据的函数"""

    def write_data(df: pd.DataFrame, in_name: str, out_name: str):
        # write the data to file
        fileutils.to_csv(df, out_name)
        append(
            result.ResultFile(
                id=id,
                current_type=current_type,
                original_filename=fileutils.get_file_name(original),
                original_filepath=original,
                in_filename=fileutils.get_file_name(in_name),
                filename=fileutils.get_file_name(out_name),
                filepath=out_name,
            )
        )

    return write_data


@validate
def compute_single(
    get_id_and_params: t.Callable[[], tuple[int, T.general.Params]],
    get_full_path: t.Callable[[str], str],
    *,
    func_set: BasicFuncSet = FuncSet(),
    is_write: bool = True,
) -> tuple[result.ComputeResult, pd.DataFrame]:
    """compute single values.

    is_write: write to file
    """
    id, params = get_id_and_params()

    input_data = InputData.from_dict(params)
    filelist: t.List[result.ResultFile] = []

    # 生成写入数据的函数
    write_data = use_write_data(
        id,
        params["udl2_file"],
        filelist.append,
        current_type=1 if is_zhiliu(params) else 0,  # ac 0, dc 1. zhiliu is dc
    )

    # filter period
    df = func_set.filter(input_data=input_data)

    if is_write:
        write_data(df, params["udl2_file"], get_full_path(params["out_file_path_1"]))

    # stat period, support multiple files, but not use this is api call
    df = (func_set.stat(df, params, interval_jihua=params.get("interval_jihua", True)),)
    df = (dict(iter(row)) for row in df)
    df = pd.DataFrame(df)

    if is_write:
        write_data(
            df, params["out_file_path_1"], get_full_path(params["out_file_path_2"])
        )

    # model period
    df = func_set.model(df, params)
    if is_write:
        write_data(
            df, params["out_file_path_2"], get_full_path(params["out_file_path_3"])
        )

    # 包含了三级文件
    file_result = result.ComputeResult(
        status=result.Status.success,
        msg="success!",
        data=filelist,
    )

    # 返回文件以及最终的DataFrame
    return file_result, df


def write_final_files(
    ac_df: pd.DataFrame, dc_df: pd.DataFrame, param_group: T.general.ParamGroup
) -> result.FinalFiles:
    """写入 ac dc 文件"""
    output_path_fn = param_group["output_path"]
    if output_path_fn is None:
        raise ValueError("output_path_fn is None")

    ac_file = output_path_fn("ac")
    dc_file = output_path_fn("dc")

    fileutils.to_csv(ac_df, str(ac_file))
    fileutils.to_csv(dc_df, str(dc_file))

    return result.FinalFiles(
        ac=result.ResultFile(
            id=1,
            current_type=0,
            original_filename="all udl2_files",
            original_filepath="null",
            in_filename="all results of udl2_files",
            filename=fileutils.get_file_name(str(ac_file)),
            filepath=str(ac_file),
        ),
        dc=result.ResultFile(
            id=2,
            current_type=1,
            original_filename="all udl2_files",
            original_filepath="null",
            in_filename="all results of udl2_files",
            filename=fileutils.get_file_name(str(dc_file)),
            filepath=str(dc_file),
        ),
    )


def collect_files(
    param_group: T.general.ParamGroup,
    is_write: bool = True,
    compute_single: T.ComputeFunc = compute_single,
) -> tuple[list[result.ComputeResult], list[pd.DataFrame]]:
    """对参数列表里面的数据进行计算，并返回结果列表"""
    res: t.List[result.ComputeResult] = []

    df_list: t.List[pd.DataFrame] = []
    for i, p in enumerate(param_group["param_list"]):

        def get_id_and_params():
            return i, p

        r, df = compute_single(
            get_id_and_params,
            param_group["get_full_path"],
            is_write=is_write,
        )
        res.append(r)
        df_list.append(df)
    return res, df_list


def compute(
    param_group: T.general.ParamGroup,
    is_write: bool = True,
    collect_files: T.CollectFilesFunc = collect_files,
) -> result.FinalResult:
    """
    计算并返回最终结果
    collect_files 是收集文件的函数，也包含了计算单个文件的过程
    """
    res, df_list = collect_files(param_group, is_write)

    # 整理最终的文件
    ac_df, dc_df = fileutils.merge_files(res, df_list)
    final_files = write_final_files(ac_df, dc_df, param_group)

    return result.FinalResult(
        status=result.Status.success,
        msg="success!",
        compute_result=res,
        final_files=final_files,
    )
