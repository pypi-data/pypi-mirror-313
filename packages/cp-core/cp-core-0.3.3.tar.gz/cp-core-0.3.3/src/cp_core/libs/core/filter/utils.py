import pandas as pd

from cp_core.libs.core.filter.fileutils import open_anko_file
from cp_core.tests.path import test2, test3
from cp_core.utils import read_csv


class FeatureUtils:
    def __init__(self):
        self.udl2_path = test3.get("udl2_path")
        self.anko_path = test3.get("anko_path")
        self.udl1_path = test2.get("udl1_path")

    def udl1_sample_data(self):
        return read_csv(self.udl1_path)

    def anko_sample_data(self):
        anko_data = open_anko_file(self.anko_path)
        return anko_data

    def udl2_sample_data(self):
        udl2_data = read_csv(self.udl2_path)
        return udl2_data
