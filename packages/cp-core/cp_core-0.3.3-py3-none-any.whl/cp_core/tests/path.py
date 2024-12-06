# coding: utf-8

"""
File Path for test.

Procedure one.
"""

import os
from cp_core.utils import is_windows  # noqa
from cp_core.config import project_root, csv_folder
import pathlib

# comment because of slow
# udl2_path = r"C:\Users\Administrator\Documents\Github\material_process\temp\371#-5#-B123# udl2_sn020736.csv"

if not isinstance(project_root, pathlib.Path):
    project_root = pathlib.Path(project_root)

# absolute csv folder path
ab_csv_path = project_root / csv_folder
udl2_path = project_root / csv_folder / "data/filter/udl2_part.csv"
prefix = pathlib.Path(project_root) / csv_folder / "data/filter/udl2+udl1"

test2 = {
    "udl2_path": f"{prefix}/udl2.csv",
    "udl1_path": f"{prefix}/udl1.csv",
    "udl1_invalid": f"{prefix}/udl1-invalid.csv",
}


test3 = {
    "udl2_path": os.path.join(
        project_root, csv_folder, r"data/filter/udl2+anko/udl2.csv"
    ),
    "anko_path": os.path.join(
        project_root, csv_folder, r"data/filter/udl2+anko/Anko.csv"
    ),
}
