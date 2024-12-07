# coding: utf-8
# author: svtter
# time: ...

""" """

import typing as t

import pandas as pd
from pydantic import BaseModel


def get_count(s: pd.Series, cond):
    return s[cond].count() / s.count() * 100


class OPMetric(BaseModel):
    """用于定义一个数值的区间范围"""

    op: t.Literal[">", ">=", "<", "<="]
    metric: float | int

    def generate_name(self, v: "Variable"):
        return f"{v.name}{self.op}{self.metric}{v.unit}的比例/%"

    def generate_count_func(self):
        """生成不同的计算函数"""

        def count_func(se):
            if self.op == ">":
                return get_count(se, se > self.metric)
            elif self.op == ">=":
                return get_count(se, se >= self.metric)
            elif self.op == "<":
                return get_count(se, se < self.metric)
            elif self.op == "<=":
                return get_count(se, se <= self.metric)

        return count_func


class Variable(BaseModel):
    """定义一个变量的名称和单位"""

    name: str
    unit: str


def stat_func(se, var: Variable, range_list: list[OPMetric]) -> list[tuple[str, float]]:
    """根据 value 生成不同的统计函数"""
    percent = [op_metric.generate_count_func()(se) for op_metric in range_list]
    res = [
        (op_metric.generate_name(var), val)
        for op_metric, val in zip(range_list, percent)
    ]
    return res
