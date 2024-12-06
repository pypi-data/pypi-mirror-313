import os

import pandas as pd
import pytest

from cp_core.utils import read_csv

from .config import RESOURCE_FOLDER


def dump_data(filename, data_list):
    with open(os.path.join(RESOURCE_FOLDER, filename), "w") as f:
        import json

        json.dump(data_list, f, ensure_ascii=False)


def dump_csv(data, filename):
    pd.DataFrame(data).to_csv(f"{RESOURCE_FOLDER}/{filename}")


@pytest.mark.skip
def test_zhiliu():
    filename = os.path.join(RESOURCE_FOLDER, "zhiliu-test.csv")
    data = read_csv(filename=filename)

    values = {"judge_metric": 0.85, "type_zhiliu": True, "is_protect": True}
    # data_list = get_all(data, judge_metrics=values["judge_metric"], values=values)
    # dump_csv(data_list, 'temp-1.csv')

    from cp_core.libs.core.stat.parse.const.ac import POLAR_NAME

    generate_folder = RESOURCE_FOLDER / "generated"

    df = data[[POLAR_NAME]]
    df.to_csv(f"{generate_folder}/temp-1.csv")
    df[POLAR_NAME] = df[POLAR_NAME][::2]
    df.to_csv(f"{generate_folder}/temp-2.csv")

    # 全部为空
    se = df[POLAR_NAME]
    assert isinstance(se, pd.Series)

    # TODO 为什么为空？
    se = se.dropna()
    assert se.empty
    se.to_csv(f"{generate_folder}/temp-4.csv")

    from cp_core.libs.core.stat.parse.dc_value import polar

    res = polar(data, values["judge_metric"], values["is_protect"], interval_jihua=True)
    dump_csv(res, "temp-3.csv")
