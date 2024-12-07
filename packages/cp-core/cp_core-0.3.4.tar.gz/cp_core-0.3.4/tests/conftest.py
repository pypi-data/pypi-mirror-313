# coding: utf-8

import os
import pathlib

import pytest

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCE_FOLDER = pathlib.Path(__file__).parent.parent / "additional_data_for_material"


@pytest.fixture
def resource_folder() -> pathlib.Path:
    return RESOURCE_FOLDER


@pytest.fixture
def base_dir() -> pathlib.Path:
    return pathlib.Path(BASE_DIR)
