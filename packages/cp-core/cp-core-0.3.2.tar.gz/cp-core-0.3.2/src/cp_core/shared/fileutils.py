from pathlib import Path

import pandas as pd


def get_output_file_encode() -> str:
    # "gbk" if windows.
    return "gbk"


def read_encode() -> str:
    return "utf8"


def to_csv(df: pd.DataFrame, target_filename: str):
    if target_filename == "":
        raise ValueError("target_filename 不能为空")
    if not target_filename.endswith(".csv"):
        raise ValueError("target_filename 必须以 .csv 结尾")

    Path(target_filename).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_filename, encoding=get_output_file_encode(), index=False)
