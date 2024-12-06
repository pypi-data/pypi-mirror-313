from pathlib import Path as _p

import pandas as pd
import pytest

from . import percent
from .const import ac as const_ac

RESOURCE_FOLDER = _p("additional_data_for_material")


def write_res(res: list[tuple[str, float]]):
    with open("./tmp/res.txt", "w", encoding="utf-8") as f:
        for r in res:
            f.write(f"{r[0]}: {r[1]}\n")


@pytest.mark.v3
def test_percent():
    df = pd.read_csv(RESOURCE_FOLDER / "v3/stat/stage-1-result.csv")

    v = percent.Variable(name=const_ac.AC_VOL_NAME, unit="V")
    se = df[v.name]
    value = [
        percent.OPMetric(op=">", metric=0.1),
        percent.OPMetric(op=">=", metric=0),
    ]
    res = percent.stat_func(se, v, value)
    assert len(res) == 2
    write_res(res)


@pytest.mark.v3
def test_op_metric():
    op_metric = percent.OPMetric(op=">", metric=0.1)
    assert (
        op_metric.generate_name(percent.Variable(name="交流电压", unit="V"))
        == "交流电压>0.1V的比例/%"
    )
