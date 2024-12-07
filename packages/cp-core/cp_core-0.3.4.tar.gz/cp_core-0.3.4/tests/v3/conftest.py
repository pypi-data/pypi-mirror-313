import pathlib

import pytest


@pytest.fixture
def resource_folder():
    return pathlib.Path(__file__).parent.parent.parent / "additional_data_for_material"


@pytest.fixture
def tmp_folder():
    return pathlib.Path(__file__).parent.parent.parent / "tmp"
