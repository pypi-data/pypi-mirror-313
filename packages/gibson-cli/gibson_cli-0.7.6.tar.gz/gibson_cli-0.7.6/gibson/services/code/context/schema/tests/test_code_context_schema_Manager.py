from gibson.services.code.context.schema.EntityKeys import EntityKeys
from gibson.services.code.context.schema.Manager import Manager


def test_get_entity_keys_no_such_entity_name():
    assert Manager().get_entity_keys("abc") is None


def test_from_code_writer_schema_context_data_dictionary():
    context = {"data": {"dictionary": {"abc": "def", "ghi": "jkl"}}, "keys": {}}

    manager = Manager().from_code_writer_schema_context(context)
    assert manager.data_dictionary.get_attribute_definition("abc") == "def"
    assert manager.data_dictionary.get_attribute_definition("ghi") == "jkl"


def test_from_code_writer_schema_context_get_entity_keys():
    context = {
        "data": {"dictionary": {}},
        "keys": {
            "abc_def": {
                "index": [],
                "primary": [
                    {"data": {"type": "pk_type_1"}, "name": "pk_name_1"},
                    {"data": {"type": "pk_type_2"}, "name": "pk_name_2"},
                ],
                "unique": [],
            }
        },
    }

    manager = Manager().from_code_writer_schema_context(context)
    assert manager.get_entity_keys("def_ghi") is None
    assert isinstance(manager.get_entity_keys("abc_def"), EntityKeys)
