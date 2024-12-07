def utils_entity_name_to_class_name(entity_name):
    parts = entity_name.split("_")

    name = []
    for part in parts:
        name.append(part.title())

    return "".join(name)


def utils_extract_module_name(entity_name):
    return entity_name.split("_")[0]


def utils_is_ref_table(entity_name):
    try:
        return entity_name.split("_")[1] == "ref"
    except IndexError:
        return False
