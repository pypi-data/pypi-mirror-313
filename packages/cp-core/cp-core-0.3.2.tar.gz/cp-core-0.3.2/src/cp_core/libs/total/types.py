import typing as t

import pandas as pd

from cp_core.libs import result
from cp_core.libs import types as general
from cp_core.libs.core.filter.forms import InputData

pd_list = list[pd.DataFrame]
result_list = list[result.ComputeResult]


class CollectFilesFunc(t.Protocol):
    def __call__(
        self, param_group: general.ParamGroup, is_write: bool
    ) -> tuple[result_list, pd_list]: ...


class ComputeFunc(t.Protocol):
    def __call__(
        self,
        get_id_and_params: t.Callable,
        get_full_path: t.Callable,
        is_write: bool,
    ) -> tuple[result.ComputeResult, pd.DataFrame]: ...


class FilterFunc(t.Protocol):
    def __call__(self, params: InputData) -> pd.DataFrame: ...


class StatFunc(t.Protocol):
    def __call__(
        self, data: pd.DataFrame, params: general.Params, is_write: bool
    ) -> pd.DataFrame: ...


class ModelFunc(t.Protocol):
    def __call__(self, data: pd.DataFrame, params: general.Params) -> pd.DataFrame: ...
