from gibson.structure.mysql.keys.IndexAttribute import IndexAttribute


def test_sql():
    index_attribute = IndexAttribute()
    index_attribute.name = "abc"

    assert index_attribute.sql() == "abc"

    index_attribute.asc = True

    assert index_attribute.sql() == "abc asc"

    index_attribute.asc = None
    index_attribute.desc = True

    assert index_attribute.sql() == "abc desc"
