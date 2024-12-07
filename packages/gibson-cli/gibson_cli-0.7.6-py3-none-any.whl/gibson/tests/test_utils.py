from gibson.core.utils import (
    utils_entity_name_to_class_name,
    utils_extract_module_name,
    utils_is_ref_table,
)


def test_entity_name_to_class_name():
    assert utils_entity_name_to_class_name("abc_def_ghi") == "AbcDefGhi"


def test_extract_module_name():
    assert utils_extract_module_name("abc_def_ghi") == "abc"


def test_is_ref_table():
    assert utils_is_ref_table("abc") is False
    assert utils_is_ref_table("abc_def") is False
    assert utils_is_ref_table("abc_ref") is True
    assert utils_is_ref_table("abc_ref_def") is True
