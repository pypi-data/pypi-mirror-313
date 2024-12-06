import os
from cp_core.config import project_root
from cp_core.libs.core.model import controller
from cp_core.libs.core.model import file
from cp_core.tests.path import csv_folder


def ab_path(path):
    return os.path.join(project_root, csv_folder, path)


def get_values() -> dict:
    path_list = (
        "data/model/jiaoliu.xlsx",
        "data/model/zhiliu-no-protect.xlsx",
        "data/model/zhiliu-protect.xlsx",
    )

    for v in path_list:
        values = {
            "in_file_path": ab_path(v),
            "type_zhiliu": 1 if v.find("zhiliu") != -1 else 0,
            "is_protect": 0 if v.find("no-protect") != -1 else 1,
        }
        yield values


def test_handle_ac_dc_data():
    for v in get_values():
        print(v)
        d = file.load_file(v.get("in_file_path"))
        res = controller.handle_ac_dc_data(d, v)
        assert res is not None, v
