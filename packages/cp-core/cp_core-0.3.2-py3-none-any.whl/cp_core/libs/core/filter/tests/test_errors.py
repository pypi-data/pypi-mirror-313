import unittest
from cp_core.libs.core.filter.errors import FileError


class ErrorTest(unittest.TestCase):
    def test_errors(self):
        def raise_exception():
            raise FileError(message=FileError.not_found)

        self.assertRaises(FileError, raise_exception)
