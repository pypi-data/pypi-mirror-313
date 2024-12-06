import pytest

from cp_core.libs.result import ComputeResult, Status
from cp_core.libs.total import validate


def test_validate():
    file_result = ComputeResult(data=[], status=Status.success, msg="")

    with pytest.raises(ValueError):
        validate.validate_files(file_result)
