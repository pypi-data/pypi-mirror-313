import pytest

from gibson.structure.Entity import Entity
from gibson.structure.mysql.Entity import Entity as MysqlEntity
from gibson.structure.postgresql.Entity import Entity as PostgresqlEntity


def test_instantiate_exceptions():
    with pytest.raises(RuntimeError) as e:
        Entity().instantiate("invalid")

    assert str(e.value) == 'unrecognized datastore type "invalid"'


def test_instantiate_mysql():
    entity = Entity().instantiate("mysql")
    assert isinstance(entity, MysqlEntity)


def test_instantiate_postgresql():
    entity = Entity().instantiate("postgresql")
    assert isinstance(entity, PostgresqlEntity)
