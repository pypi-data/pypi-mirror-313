import pytest

from gibson.structure.mysql.constraints.ReferenceConstraint import ReferenceConstraint
from gibson.structure.mysql.Entity import Entity
from gibson.structure.mysql.keys.ForeignKey import ForeignKey
from gibson.structure.mysql.keys.Index import Index
from gibson.structure.mysql.testing import (
    structure_testing_get_entity,
    structure_testing_get_struct_data,
)


def test_add_foreign_key():
    reference_constraint = ReferenceConstraint()
    reference_constraint.attributes = ["a", "b"]
    reference_constraint.references = "abc_def"

    foreign_key = ForeignKey()
    foreign_key.attributes = ["c", "d"]
    foreign_key.reference = reference_constraint

    entity = structure_testing_get_entity()
    entity.add_foreign_key(foreign_key)

    assert entity.keys["foreign"] == [
        {
            "attributes": ["c", "d"],
            "datastore": {
                "specifics": {
                    "name": None,
                    "relationship": {"type": None},
                    "symbol": None,
                }
            },
            "references": {
                "attributes": ["a", "b"],
                "datastore": {
                    "specifics": {
                        "match": None,
                    }
                },
                "entity": {"name": "abc_def", "schema_": None},
                "on": {"delete": None, "update": None},
                "sql": "references abc_def (a, b)",
            },
            "sql": "foreign key (c, d) references abc_def (a, b)",
        }
    ]


def test_add_attribute_after():
    entity = structure_testing_get_entity()
    entity.add_attribute("abc", "bigint", after="uuid")

    assert entity.attributes[2]["sql"] == "abc bigint"


def test_add_attribute_before():
    entity = structure_testing_get_entity()
    entity.add_attribute("abc", "bigint", before="uuid")

    assert entity.attributes[1]["sql"] == "abc bigint"


def test_add_attribute_append():
    entity = structure_testing_get_entity()
    entity.add_attribute("abc", "bigint")

    assert entity.attributes[-1]["sql"] == "abc bigint"


def test_add_index():
    index = Index()
    index.add_attribute("abc")
    index.add_attribute("def")

    entity = structure_testing_get_entity()
    entity.add_index(index)

    assert entity.keys["index"] == [
        {
            "attributes": ["abc", "def"],
            "datastore": {
                "specifics": {
                    "name": None,
                    "using": None,
                }
            },
            "sql": "index (abc, def)",
        }
    ]


def test_import_from_struct_incorrect_data_format():
    with pytest.raises(RuntimeError) as e:
        Entity().import_from_struct({"abc": "def"})

    assert str(e.value) == "cannot import from struct, incorrect data format"


def test_import_from_struct():
    entity = Entity().import_from_struct(structure_testing_get_struct_data())

    assert entity.name == "abc_def"
    assert len(entity.attributes) == 4
    assert entity.attributes[0]["name"] == "id"
    assert entity.attributes[1]["name"] == "uuid"
    assert entity.attributes[2]["name"] == "date_created"
    assert entity.attributes[3]["name"] == "date_updated"
    assert entity.constraints == {"check": []}
    assert entity.keys == {"foreign": [], "index": [], "primary": None, "unique": []}
    assert entity.table == {
        "parameters": {
            "auto": None,
            "charset": None,
            "collate": None,
            "default": None,
            "engine": None,
            "sql": None,
        }
    }
