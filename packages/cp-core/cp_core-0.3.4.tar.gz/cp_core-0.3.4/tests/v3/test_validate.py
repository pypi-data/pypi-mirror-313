import typing as t

import pandas as pd
import pytest

from cp_core.libs.result import ComputeResult, ResultFile, Status
from cp_core.libs.total.validate import validate


@pytest.fixture
def result_files() -> t.List[ResultFile]:
    return [
        ResultFile(
            id=1,
            current_type=0,
            original_filename="test",
            original_filepath="test",
            in_filename="test",
            filename="file",
            filepath="file",
        ),
        ResultFile(
            id=1,
            current_type=0,
            original_filename="test",
            original_filepath="test",
            in_filename="test",
            filename="file",
            filepath="file",
        ),
        ResultFile(
            id=1,
            current_type=0,
            original_filename="test",
            original_filepath="test",
            in_filename="test",
            filename="file",
            filepath="file",
        ),
    ]


def test_validate(result_files: t.List[ResultFile]):
    @validate
    def custom_func(*, is_write: bool = True):
        if is_write:
            return (
                ComputeResult(
                    status=Status.success,
                    msg="success",
                    data=result_files[:1],
                ),
                pd.DataFrame(),
            )
        return ComputeResult(
            status=Status.success,
            msg="success",
            data=[],
        ), pd.DataFrame()

    with pytest.raises(ValueError):
        custom_func(is_write=True)

    custom_func(is_write=False)
