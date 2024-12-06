# coding: utf-8
# author: svtter
# time: ...

""" """

import typing as t

from pydantic import BaseModel


class Zhiliu(BaseModel):
    type_zhiliu: bool = False


class Protect(BaseModel):
    is_protect: bool = False


def is_zhiliu(values: dict | t.Any):
    zhiliu = Zhiliu.model_validate(values)
    return zhiliu.type_zhiliu


def is_protect(values: dict | t.Any):
    protect = Protect.model_validate(values)
    return protect.is_protect
