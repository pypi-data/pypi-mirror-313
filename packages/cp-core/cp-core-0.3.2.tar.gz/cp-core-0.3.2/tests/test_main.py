import os
import pathlib
import unittest
from cp_core.config import project_root


def build():
    pass


def clean():
    pass


class MainTest(unittest.TestCase):
    @unittest.skip(reason="for windows only")
    def test_exec_p5(self):
        """ """

        exe = pathlib.Path(project_root) / "dist/main/main.exe"
        json_file = (
            pathlib.Path(project_root)
            / "process/libs/validator/tests/json_test/p5/base.json"
        )
        res = os.system(str(exe) + " --f " + str(json_file))
        self.assertEqual(res, 0, msg=res)
        self.assertTrue(os.path.exists("res.json"))
        os.remove("res.json")
