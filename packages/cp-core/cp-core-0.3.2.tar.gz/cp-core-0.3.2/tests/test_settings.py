from cp_core import settings


def test_settings_parse():
    k, v = settings.parse("hello=[1]")

    assert k == ["hello"]
    assert v == [1]

    keys, v = settings.parse("dcie.level_low.[1]=[12]")

    assert keys == ["dcie", "level_low", "[1]"]
    assert v == [12]


def test_assign():
    old = settings.default_settings.copy()

    keys, v = settings.parse("dcie.level_low.[1]=[12]")
    s = settings.assign(settings.default_settings, keys, v)

    assert s == old
    assert s["dcie"]["level_low"][0]["value"] == [12]

    keys, v = settings.parse("dcie.level_low.[2]=[12]")
    s = settings.assign(settings.default_settings, keys, v)
    assert s["dcie"]["level_low"][1]["value"] == [12]


def test_parse_and_assign():
    s = settings.parse_and_assign(settings.default_settings, "dcie.level_high.[1]=[12]")
    assert s["dcie"]["level_high"][0]["value"] == [12]
