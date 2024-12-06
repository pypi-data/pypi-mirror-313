import typing as t

import pandas as pd

from cp_core.libs.core.filter import extract, forms

# src\cp_core\libs\core\model\controller.py
from cp_core.libs.core.model import controller
from cp_core.libs.core.stat import merge
from cp_core.libs.total import fileutils
from cp_core.libs.total import types as T
from cp_core.libs.total.controller import BasicFuncSet


@forms.validate_filename
def filter_process(input_data: forms.InputData) -> pd.DataFrame:
    data = fileutils.read_first_file(input_data.udl2_file)
    res_data = extract.extract_data_from_udl2(data, input_data)
    return res_data


def stat_process(data: pd.DataFrame, params: T.general.Params):
    """
    main method for statistic process
    """
    res_data = merge.generate_row_from_data(
        data,
        params,
        interval_jihua=params["interval_jihua"],
    )

    # generate data frame
    res = dict(res_data)
    df = pd.DataFrame([res])
    return df


def model_process(data, values: T.general.ModelParams) -> pd.DataFrame:
    return controller.handle_ac_dc_data(data, values)


class FunSetV2(BasicFuncSet):
    def filter(self, data: pd.DataFrame, input_data: forms.InputData, *args, **kwargs):
        return filter_process(input_data)

    def stat(self, data: pd.DataFrame, params: T.general.Params, *args, **kwargs):
        return stat_process(data, params)

    def model(self, data: pd.DataFrame, params: T.general.ModelParams, *args, **kwargs):
        return model_process(data, params)
