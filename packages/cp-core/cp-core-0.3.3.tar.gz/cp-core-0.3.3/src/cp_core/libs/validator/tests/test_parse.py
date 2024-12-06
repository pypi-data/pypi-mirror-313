# coding: utf-8
import json
import os
import pathlib
import unittest
from typing import Iterable, List

import pytest

from cp_core.config import project_root
from cp_core.libs.validator.parse import process_values
from cp_core.tests.path import csv_folder


class ParseTest(unittest.TestCase):
    """测试处理 json 数据"""

    def test_process_values(self):
        # 检验前三个过程的数据
        for pname in ("p1", "p2", "p3"):
            values_list = get_config(name=pname)

            for v in values_list:
                self.assert_process_values(v, pname)
                outfile = v.get("out_file_path")
                self.assert_file(outfile)

    def test_process_values_p4(self):
        for value in get_config(name="p4"):
            self.assert_process_values(value)
            for path in out_file_list(value):
                self.assert_file(path)

    @pytest.mark.skip(
        "之前的测试都没发现问题。现在使用 pydantic 找到了输入数据的问题。还需要再验证。"
    )
    def test_process_values_p5(self):
        for value in get_config(name="p5"):
            self.assert_process_values(value)
            p = value.get("output")
            self.assert_file(p)

    def assert_file(self, path):
        if not isinstance(path, str):
            self.fail(f"path, type is [{type(path)}] is not a str.")
        assert os.path.exists(path)
        os.remove(path)

    def assert_process_values(self, v, pname=None):
        # 捕获异常
        res = process_values(v)
        if not res.is_success():
            res.msg_to_file("./tmp/p5msg.txt")
        self.assertTrue(res.is_success(), msg=(pname, res.msg, v, pname))


def ab_path(path: str) -> pathlib.Path:
    return project_root / path


def get_json(filename):
    with open(filename) as f:
        res = json.load(f)
    return res


def get_config(name: str) -> List[dict]:
    """从 file dict 中读取对应的字段，来进行测试

    Args:
        name (str): _description_

    Raises:
        Exception: _description_

    Returns:
        list: _description_
    """
    prefix = ab_path(csv_folder)
    file_dict = json.loads((prefix / "json_test" / "file_dict.json").read_text())
    file_list = file_dict.get(name, None)
    if not file_list:
        raise TypeError(f"not such name: {name}. Should be in p1/p2/p3/p4/p5")

    # 拼接前缀，读取 json 数据
    def custom_join(prefix, filename) -> str:
        return str(pathlib.Path(prefix) / filename)

    file_list = [custom_join(prefix, filename) for filename in file_list]
    return [get_json(filename) for filename in file_list]


def out_file_list(v) -> Iterable[str]:
    file_list = ("out_file_path_1", "out_file_path_2", "out_file_path_3")
    for filename in file_list:
        path = v.get(filename)
        if not isinstance(path, str):
            raise Exception("not a valid path")
        yield path
