import pytest

from cp_core.libs.core.filter import extract, forms
from cp_core.libs.core.filter.parse.night import add_night_data
from cp_core.utils import read_csv


@pytest.mark.skip("no test-2.csv file.")
def test_night(resource_folder):
    csv_file = resource_folder / "test-2.csv"

    df = read_csv(csv_file)
    df = extract.extract_data_from_udl2(df, area=1)

    conf = forms.InputData(
        device_id=2,
        resistivity=1,
        piece_id=1,
        piece_area=1,
        udl2_file=csv_file,
        udl1_file=None,
        out_file_path=resource_folder / "test.csv",
    )

    df = add_night_data(
        df,
        conf,
        need=["piece_area", "piece_id", "resistivity", "device_id"],
        names=["试片面积(cm^2)", "试片编号", "土壤电阻率(Ω*m)", "测试桩编号"],
    )
    df.to_csv(resource_folder / "test-result.csv")

    # df = add_night(df)
