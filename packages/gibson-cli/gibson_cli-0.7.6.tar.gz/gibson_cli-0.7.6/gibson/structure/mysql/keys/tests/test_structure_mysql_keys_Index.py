import pytest

from gibson.structure.mysql.keys.Index import Index


def test_sql_exceptions():
    with pytest.raises(RuntimeError) as e:
        Index().sql()

    assert str(e.value) == "index is missing attributes"


def test_sql_1():
    index = Index()
    index.add_attribute("a").add_attribute("b")

    assert index.sql() == "index (a, b)"

    index.name = "abc_def_idx"

    assert index.sql() == "index abc_def_idx (a, b)"

    index.using = "btree"

    assert index.sql() == "index abc_def_idx using btree (a, b)"


def test_sql_2():
    index = Index()
    index.add_attribute("a").add_attribute("b")
    index.using = "hash"

    assert index.sql() == "index using hash (a, b)"


def test_add_attribute_asc_and_desc_exception():
    with pytest.raises(RuntimeError) as e:
        Index().add_attribute("abc", True, True)

    assert str(e.value) == "an index attribute cannot be both asc and desc"


def test_add_attribute_asc():
    index = Index()
    index.add_attribute("a", True)

    assert index.sql() == "index (a asc)"

    index = Index()
    index.add_attribute("a", asc=True)

    assert index.sql() == "index (a asc)"


def test_add_attribute_desc():
    index = Index()
    index.add_attribute("a", False, True)

    assert index.sql() == "index (a desc)"

    index = Index()
    index.add_attribute("a", desc=True)

    assert index.sql() == "index (a desc)"


def test_attribute_name_list():
    index = Index()
    index.add_attribute("a").add_attribute("b")

    assert index.attribute_name_list() == ["a", "b"]


def test_reset_attributes():
    index = Index()
    index.add_attribute("a").add_attribute("b")

    assert len(index.attributes) == 2
    assert index.attribute_name_list() == ["a", "b"]

    index.reset_attributes()

    assert index.attributes is None
    assert index.attribute_name_list() == []


def test_json():
    index = Index()
    index.add_attribute("a").add_attribute("b")
    index.name = "abc_def_idx"
    index.using = "btree"

    assert index.json() == {
        "attributes": ["a", "b"],
        "datastore": {
            "specifics": {
                "name": "abc_def_idx",
                "using": "btree",
            }
        },
        "sql": "index abc_def_idx using btree (a, b)",
    }
