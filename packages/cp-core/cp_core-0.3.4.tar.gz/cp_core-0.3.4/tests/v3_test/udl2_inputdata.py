import pandas as pd

from cp_core.libs import types as T
from cp_core.libs.core.filter.forms import InputData
from cp_core.v3.config import RESOURCE_FOLDER

values = InputData(
    device_id="371",
    resistivity=1,
    piece_id="B123",
    piece_area=1,
    udl1_file="",
    udl2_file=str(RESOURCE_FOLDER / "data/filter/udl2_DW06-20057.csv"),
    out_file_path="",
)

params: T.Params = {
    "period": 4,
    "types": 0,
    "type_zhiliu": 0,
    "is_protect": 0,
    "device_id": "#11",
    "piece_id": "#11",
    "piece_area": 10.0,
    "resistivity": 10.0,
    "judge_metric": 10.0,
    "udl2_file": str(values.udl2_file),
    "udl1_file": "",
    "interval_jihua": False,
    "out_file_path_1": "temp1.csv",
    "out_file_path_2": "temp2.csv",
    "out_file_path_3": "temp3.csv",
}
