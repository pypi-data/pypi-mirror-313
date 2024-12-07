"""
12、如果在分步模式第二步“统计数据分析”中若不勾选“阴极保护”选项，且上一级文件中“夜间极化电位”缺失，则第10条对应的列所有数据均显示“——”或“数据缺失”，若勾选“阴极保护”，则取-850V；
"""

import pytest

from cp_core.api import compute
from cp_core.libs.types import ParamGroup, Params


@pytest.mark.v3
@pytest.mark.parametrize(
    "filename",
    [
        # "AF042 udl2_sn023296.csv",
        # "自研设备的数据文件-udl2.csv",
        # "从AF042中提取的部分数据-udl2.csv",
        "GHGX002-udl2.csv",
    ],
)
def test_missing_data(resource_folder, tmp_folder, filename):
    udl2_path = resource_folder / "v3" / "real" / "day-1203" / filename
    assert udl2_path.exists()

    import uuid
    from datetime import datetime

    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + str(uuid.uuid4())[:5]

    params = ParamGroup(
        output_path=lambda x: str(tmp_folder / current_date / f"result-{x}.csv"),
        get_full_path=lambda x: str(tmp_folder / current_date / x),
        param_list=[
            Params(
                device_id="test",
                resistivity=1,
                piece_id="test",
                piece_area=1,
                type_zhiliu=True,
                is_protect=False,
                judge_metric=-0.85,
                udl2_file=str(udl2_path),
                udl1_file="",
                out_file_path_1=str(tmp_folder / current_date / "out1-dc.csv"),
                out_file_path_2=str(tmp_folder / current_date / "out2-dc.csv"),
                out_file_path_3=str(tmp_folder / current_date / "out3-dc.csv"),
            ),
            Params(
                device_id="test",
                resistivity=1,
                piece_id="test",
                piece_area=1,
                type_zhiliu=False,
                is_protect=False,
                judge_metric=-0.85,
                udl2_file=str(udl2_path),
                udl1_file="",
                out_file_path_1=str(tmp_folder / current_date / "out1-ac.csv"),
                out_file_path_2=str(tmp_folder / current_date / "out2-ac.csv"),
                out_file_path_3=str(tmp_folder / current_date / "out3-ac.csv"),
            ),
        ],
    )

    compute(params, is_write=True)
