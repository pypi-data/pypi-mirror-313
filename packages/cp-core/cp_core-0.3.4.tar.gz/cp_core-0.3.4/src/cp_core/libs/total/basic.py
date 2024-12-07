import abc
import typing as t


class BasicFuncSet(abc.ABC):
    filter: t.Callable
    stat: t.Callable
    model: t.Callable
