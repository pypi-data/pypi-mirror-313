import pytest

from gibson.structure.postgresql.Entity import Entity
from gibson.structure.postgresql.References import References
from gibson.structure.postgresql.table.ForeignKey import ForeignKey
from gibson.structure.postgresql.testing import (
    structure_testing_get_entity,
    structure_testing_get_struct_data,
)


def test_add_foreign_key():
    references = References()
    references.columns = ["a", "b"]
    references.ref_table = "abc_def"

    foreign_key = ForeignKey()
    foreign_key.columns = ["c", "d"]
    foreign_key.references = references

    entity = structure_testing_get_entity()
    entity.add_foreign_key(foreign_key)

    assert entity.keys["foreign"] == [
        {
            "attributes": ["c", "d"],
            "references": {
                "attributes": ["a", "b"],
                "datastore": {
                    "specifics": {
                        "match": {"full": None, "partial": None, "simple": None}
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
    assert entity.table is None
