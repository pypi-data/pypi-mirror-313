import typing as t

from cp_core.libs import types as T
from cp_core.libs.result import Result


class UseFilter(t.Protocol):
    def __call__(self, v: T.FilterParams) -> Result: ...


class UseStat(t.Protocol):
    def __call__(self, v: T.StatParams) -> Result: ...


class UseModel(t.Protocol):
    def __call__(self, v: T.ModelParams) -> Result: ...
