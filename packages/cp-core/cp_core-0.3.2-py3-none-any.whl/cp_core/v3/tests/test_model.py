import pandas as pd
import pytest

from cp_core.v3 import const, model
from cp_core.v3.config import RESOURCE_FOLDER


@pytest.mark.v3
@pytest.mark.parametrize("is_protect", [0, 1])
def test_get_all_ac(is_protect):
    df = pd.read_csv(
        RESOURCE_FOLDER / f"v3/real/stage-2-result-ac-protect-{is_protect}.csv"
    )
    df = model.predict_ac(df)
    df.to_csv(
        RESOURCE_FOLDER / f"v3/real/stage-3-result-ac-protect-{is_protect}.csv",
        index=False,
    )
    assert const.POLAR_005_03 in df.keys()


@pytest.mark.v3
@pytest.mark.parametrize("is_protect", [0, 1])
def test_predict_dc(tmp_folder, is_protect):
    df = pd.read_csv(tmp_folder / f"stage-2-result-dc-protect-{is_protect}.csv")
    df = model.predict_dc(df, is_protect=is_protect)
    df.to_csv(
        tmp_folder / f"stage-3-result-dc-protect-{is_protect}.csv",
        index=False,
    )

    want = [
        "极化电位(V_CSE)_min",
        *([const.POLAR_NIGHT_20MV] if not is_protect else []),
    ]
    assert set(want) <= set(df.keys())
