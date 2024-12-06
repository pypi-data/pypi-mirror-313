import pytest


@pytest.mark.python_knowledge
def test_tuple_expand():
    test = False
    my_t = ("a", "b", *("c" if test else []))
    assert my_t == ("a", "b")
