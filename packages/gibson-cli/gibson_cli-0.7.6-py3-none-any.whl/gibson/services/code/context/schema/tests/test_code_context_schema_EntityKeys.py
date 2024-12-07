from gibson.services.code.context.schema.EntityKeys import EntityKeys
from gibson.structure.mysql.constraints.ReferenceConstraint import ReferenceConstraint
from gibson.structure.mysql.keys.ForeignKey import ForeignKey
from gibson.structure.mysql.keys.Index import Index


def test_best_sql_foreign_key_no_match():
    assert EntityKeys().best_sql_foreign_key() is None


def test_best_sql_foreign_key_choose_primary():
    ek = EntityKeys().from_code_writer_schema_context(
        "abc",
        [],
        [
            {"data": {"type": "pk_type_1"}, "name": "pk_name_1"},
            {"data": {"type": "pk_type_2"}, "name": "pk_name_2"},
        ],
        [{"data": {"type": "uk_type_1"}, "name": "uk_name_1"}],
    )

    foreign_key, index, data_types = ek.best_sql_foreign_key()
    assert isinstance(foreign_key, ForeignKey)
    assert isinstance(foreign_key.reference, ReferenceConstraint)
    assert isinstance(index, Index)
    assert foreign_key.attributes == ["abc_pk_name_1", "abc_pk_name_2"]
    assert foreign_key.reference.attributes == ["pk_name_1", "pk_name_2"]
    assert foreign_key.reference.references == "abc"
    assert len(index.attributes) == 2
    assert index.attributes[0].name == "abc_pk_name_1"
    assert index.attributes[1].name == "abc_pk_name_2"
    assert len(data_types) == 2
    assert data_types[0] == "pk_type_1"
    assert data_types[1] == "pk_type_2"


def test_best_sql_foreign_key_choose_unique():
    ek = EntityKeys().from_code_writer_schema_context(
        "abc", [], [], [{"data": {"type": "uk_type_1"}, "name": "uk_name_1"}]
    )

    foreign_key, index, data_types = ek.best_sql_foreign_key()
    assert isinstance(foreign_key, ForeignKey)
    assert isinstance(foreign_key.reference, ReferenceConstraint)
    assert isinstance(index, Index)
    assert foreign_key.attributes == ["abc_uk_name_1"]
    assert foreign_key.reference.attributes == ["uk_name_1"]
    assert foreign_key.reference.references == "abc"
    assert len(index.attributes) == 1
    assert index.attributes[0].name == "abc_uk_name_1"
    assert len(data_types) == 1
    assert data_types[0] == "uk_type_1"
