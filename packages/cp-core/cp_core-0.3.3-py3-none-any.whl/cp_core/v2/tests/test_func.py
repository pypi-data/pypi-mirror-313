import pandas as pd
import pytest

from cp_core.libs.core.filter.errors import EmptyError
from cp_core.v2 import func


def test_empty():
    @func.empty_checker(name="test")
    def my_func():
        df = pd.DataFrame({})
        assert df.empty
        return df

    with pytest.raises(EmptyError):
        df = pd.DataFrame({})
        assert df.empty
        func.is_empty(df, "test")

    with pytest.raises(EmptyError):
        my_func()
