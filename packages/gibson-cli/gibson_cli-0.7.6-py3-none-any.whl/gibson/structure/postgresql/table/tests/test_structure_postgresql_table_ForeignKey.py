import pytest

from gibson.structure.postgresql.References import References
from gibson.structure.postgresql.table.ForeignKey import ForeignKey


def test_sql():
    references = References()
    references.columns = ["a", "b"]
    references.ref_table = "other_table"

    foreign_key = ForeignKey()
    foreign_key.references = references

    foreign_key.columns = ["a", "b"]

    assert foreign_key.sql() == "foreign key (a, b) references other_table (a, b)"


def test_json():
    references = References()
    references.columns = ["a", "b"]
    references.match_full = True
    references.match_partial = False
    references.match_simple = True
    references.ref_table = "other_table"

    foreign_key = ForeignKey()
    foreign_key.columns = ["c", "d"]
    foreign_key.references = references

    assert foreign_key.json() == {
        "attributes": ["c", "d"],
        "references": {
            "attributes": ["a", "b"],
            "datastore": {
                "specifics": {"match": {"full": True, "partial": False, "simple": True}}
            },
            "entity": {"name": "other_table", "schema_": None},
            "on": {"delete": None, "update": None},
            "sql": "references other_table (a, b) match full match simple",
        },
        "sql": "foreign key (c, d) references other_table (a, b) match full match simple",
    }
