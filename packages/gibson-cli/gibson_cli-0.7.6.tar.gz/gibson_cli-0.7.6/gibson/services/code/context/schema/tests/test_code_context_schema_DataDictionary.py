from gibson.services.code.context.schema.DataDictionary import DataDictionary


def test_configure():
    data_dict = DataDictionary().from_code_writer_schema_context({"a": "b", "c": "d"})
    assert data_dict.get_attribute_definition("z") is None
    assert data_dict.get_attribute_definition("a") == "b"
    assert data_dict.get_attribute_definition("c") == "d"
