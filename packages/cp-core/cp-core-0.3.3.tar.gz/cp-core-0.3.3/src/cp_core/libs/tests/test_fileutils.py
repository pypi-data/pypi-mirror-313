from cp_core.libs.total import fileutils as f


def test_get_file_name():
    assert f.get_file_name("/tmp/temp-11-merge.csv") == "temp-11-merge.csv"
    assert f.get_file_name("/tmp/temp-11-merge.xlsx") == "temp-11-merge.xlsx"
    assert f.get_file_name("/tmp/tmp/temp-11-merge.xls") == "temp-11-merge.xls"
