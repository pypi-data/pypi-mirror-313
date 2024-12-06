# coding: utf-8

import os
import pathlib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCE_FOLDER = pathlib.Path(__file__).parent.parent / "additional_data_for_material"
