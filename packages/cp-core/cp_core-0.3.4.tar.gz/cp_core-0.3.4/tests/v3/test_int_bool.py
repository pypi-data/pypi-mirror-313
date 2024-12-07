import pytest


@pytest.mark.python_knowledge
def test_int_bool():
    protect = 1
    if protect:
        assert 1 == 1
    else:
        assert 1 == 2
