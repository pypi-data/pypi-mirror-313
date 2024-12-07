import pytest


@pytest.mark.skip("Not finished.")
def test_tiny_db():
    from tinydb import Query, TinyDB

    db = TinyDB("additional_data_for_material/json_test/p1-anko.json")
    table = db.table("p_data")
    assert False, table.all()
