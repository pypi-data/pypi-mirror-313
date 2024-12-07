import pytest

from gibson.structure.mysql.constraints.ReferenceConstraint import ReferenceConstraint
from gibson.structure.mysql.keys.ForeignKey import ForeignKey


def test_sql_exceptions():
    with pytest.raises(RuntimeError) as e:
        ForeignKey().sql()

    assert str(e.value) == "foreign key is missing attributes"

    foreign_key = ForeignKey()
    foreign_key.attributes = ["a"]

    with pytest.raises(RuntimeError) as e:
        foreign_key.sql()

    assert str(e.value) == "reference must be instance of ReferenceConstraint"

    foreign_key.reference = "abc"

    with pytest.raises(RuntimeError) as e:
        foreign_key.sql()

    assert str(e.value) == "reference must be instance of ReferenceConstraint"


def test_sql():
    reference = ReferenceConstraint()
    reference.attributes = ["a", "b"]
    reference.references = "other_table"

    foreign_key = ForeignKey()
    foreign_key.reference = reference

    foreign_key.attributes = ["a", "b"]

    assert foreign_key.sql() == "foreign key (a, b) references other_table (a, b)"

    foreign_key.name = "abc_def_fk"

    assert foreign_key.sql() == (
        "foreign key abc_def_fk (a, b) references other_table (a, b)"
    )

    foreign_key.symbol = "foreign_key_symbol"

    assert foreign_key.sql() == (
        "constraint foreign_key_symbol foreign key abc_def_fk (a, b) "
        + "references other_table (a, b)"
    )


def test_json():
    reference = ReferenceConstraint()
    reference.attributes = ["a", "b"]
    reference.references = "other_table"

    foreign_key = ForeignKey()
    foreign_key.attributes = ["c", "d"]
    foreign_key.name = "abc_def_fk"
    foreign_key.reference = reference
    foreign_key.symbol = "foreign_key_symbol"

    assert foreign_key.json() == {
        "attributes": ["c", "d"],
        "datastore": {
            "specifics": {
                "name": "abc_def_fk",
                "relationship": {"type": None},
                "symbol": "foreign_key_symbol",
            }
        },
        "references": {
            "attributes": ["a", "b"],
            "datastore": {
                "specifics": {
                    "match": None,
                }
            },
            "entity": {"name": "other_table", "schema_": None},
            "on": {"delete": None, "update": None},
            "sql": "references other_table (a, b)",
        },
        "sql": "constraint foreign_key_symbol foreign key abc_def_fk (c, d) "
        + "references other_table (a, b)",
    }
