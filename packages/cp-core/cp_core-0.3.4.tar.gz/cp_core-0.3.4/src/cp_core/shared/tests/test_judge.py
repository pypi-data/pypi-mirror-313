from cp_core.shared import judge


def test_is_protect():
    assert judge.is_protect({"is_protect": True})
    assert not judge.is_protect({"is_protect": False})
