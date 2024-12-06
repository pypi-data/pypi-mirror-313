# coding: utf-8
# author: svtter
# time: ...

"""
"""


import unittest
from .base import get_data


class PercentTestor(unittest.TestCase):
    def setUp(self) -> None:
        self.data = get_data()
