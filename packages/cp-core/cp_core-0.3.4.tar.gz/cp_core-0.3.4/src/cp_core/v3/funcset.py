import typing as t

import pandas as pd

from cp_core.libs import types as T
from cp_core.libs.core.filter import fileutils, forms
from cp_core.libs.core.filter.parse.const import NIGHT_NAME
from cp_core.libs.core.stat.merge import (
    generate_row_from_data as stat_process,
)
from cp_core.libs.total.basic import BasicFuncSet
from cp_core.libs.types import ModelParams
from cp_core.shared.judge import is_protect, is_zhiliu

from . import extract, model, stat


class FuncSetV3(BasicFuncSet):
    """v3 version of cp-core
    只需要实现 funcset, 就可以实现新的计算方法。
    """

    def model(self, data: pd.DataFrame, values: ModelParams):
        if is_zhiliu(values):
            df = model.predict_dc(data, is_protect(values))
        else:
            df = model.predict_ac(data)
        return df

    def stat(self, data: pd.DataFrame, params: T.Params, interval_jihua: bool = False):
        return stat_process(data, params, interval_jihua, func_set=stat.StatFuncSetV3)

    def filter(self, input_data: forms.InputData, *args, **kwargs):
        # from cp_core.libs.core.filter.parse import const
        from cp_core.v3 import const

        data = fileutils.read_first_file(input_data.udl2_file)

        # 使用 v1 版本的数据提取
        df = extract.extract_data_from_udl2(data, input_data, *args, **kwargs)

        # 原本的数值重新命名
        df[const.NIGHT_NAME] = df[const.NIGHT_NAME_OLD]

        # previous get data func.
        night = extract.obtain_night_data(data)

        # 整理最终列
        columns_names = [
            "测试桩编号",
            "土壤电阻率(Ω*m)",
            "试片编号",
            "试片面积(cm^2)",
            const.DATE_NAME,
            const.POWER_ON_NAME,
            const.POLAR_NAME,
            const.DC_CURRENT_NAME,
            const.DC_CURRENT_DENSITY_NAME,
            const.AC_CURRENT_NAME,
            const.AC_VOL_NAME,
            const.AC_CURRENT_DENSITY_NAME,
            # const.NIGHT_NAME,
            const.NIGHT_POWERON,
            const.NIGHT_POLAR_AVG,
            const.STATUS_NAME,
        ]
        df = pd.merge(df, night, on=const.DATE_NAME, how="outer")
        df = df.reindex(columns=columns_names)
        return df
