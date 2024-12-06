import pathlib

import pandas as pd

from comprehensive.config import MetaName, Options
from cp_core.libs.comprehensive.controller import (
    comprehensive_controller,
)
from cp_core.utils import read_csv


def mapping_to(ch: str) -> int:
    map_dict = {
        "高": 1,
        "中": 0,
        "低": -1,
        "有": 1,
        "无": 0,
        "欠保护": -1,
        "达标": 0,
        "过保护": 1,
        "空": -10,
    }
    return map_dict[ch]


def mapping_to_by_dict(values: dict) -> dict:
    """
    map the chinese str to number
    """
    new_v = {}
    for k, v in values.items():
        if v:
            new_v[k] = mapping_to(v)

    # add an empty string for output path compatible
    new_v["output"] = "no use"
    return new_v


def change_text(window, key, value) -> None:
    """change the text in window"""
    window.Element(key).update(value)


def open_file(file_path: str) -> pd.DataFrame:
    """
    use pandas open csv file.
    """
    p = pathlib.Path(file_path)
    if not p.exists():
        raise Exception(f"filepath: {p} not such file.")

    if file_path.endswith(".csv"):
        return read_csv(p)
    raise Exception(f"{p} is not a CSV file.")


def comp_map(se: pd.Series) -> pd.Series:
    result = comprehensive_controller(dict(se), write=False)
    if result == "success":
        se[MetaName.result] = result.value
    return se


def compute_res(df: pd.DataFrame) -> pd.DataFrame:
    """
    compute the final result
    """
    return df.apply(comp_map, axis="columns")


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    transform the origin data.
    """
    return df.applymap(mapping_to)


def gen_tables() -> pd.DataFrame:
    data = {
        MetaName.corrosive: [Options.corrosive[0], Options.corrosive[1]],
        MetaName.detect: [Options.detect[0], Options.detect[1]],
        MetaName.protect: [Options.protect[0], Options.protect[1]],
        MetaName.ac: [Options.ac[0], Options.ac[1]],
        MetaName.dc: [Options.dc[0], Options.dc[1]],
        MetaName.result: [Options.result[0], Options.result[1]],
    }
    df = pd.DataFrame(data=data)
    return df


def update_df_result(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.pipe(transform_data).pipe(compute_res)
    df[[MetaName.result]] = new_df[[MetaName.result]].applymap(trans_back)
    return df


def write_file(df: pd.DataFrame, name: str):
    df.to_csv(name, encoding="gbk", index=False)


def trans_back(val: int) -> str:
    res = {1: "高", 0: "中", -1: "低"}[val]
    return res
