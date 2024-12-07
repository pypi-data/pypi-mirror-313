import unittest


class Utils:
    @classmethod
    def print(cls, a):
        print(a)


class CLSTest(unittest.TestCase):
    def test_something(self):
        pass

    def test_utils(self):
        cc = Utils.print
        cc("hello")
