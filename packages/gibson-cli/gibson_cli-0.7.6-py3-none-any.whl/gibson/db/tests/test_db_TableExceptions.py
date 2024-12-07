from gibson.db.TableExceptions import TableExceptions


def test_universal():
    assert TableExceptions().universal() == ["alembic_version"]


def test_mysql():
    assert TableExceptions().mysql() == ["alembic_version"]


def test_postgresql():
    assert TableExceptions().postgresql() == ["alembic_version"]
