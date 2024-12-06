"""
Make config file here.

Thisi file is to store programming config.
"""

import ast
import os
import pathlib

from loguru import logger

DEBUG = ast.literal_eval(os.getenv("CORE_DEBUG", "False"))

# logger.setLevel(logging.DEBUG)
if not DEBUG:
    logger.add("info.log")


# generate project root.
project_root = pathlib.Path(__file__).parent.parent.parent

csv_folder = "additional_data_for_material"

udl2_file_keys = [
    "Record Type",
    "Date/Time(中国标准时间)",
    "Potential DC Reading",
    "Potential DC Units",
    "Potential DC Instant Off Reading",
    "Potential DC Instant Off Units",
    "Potential AC Reading",
    "Potential AC Units",
    "Current DC Reading",
    "Current DC Units",
    "Current AC Reading",
    "Current AC Units",
]
