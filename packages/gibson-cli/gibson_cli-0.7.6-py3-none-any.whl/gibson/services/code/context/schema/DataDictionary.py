class DataDictionary:
    def __init__(self):
        self.__attributes = {}

    def from_code_writer_schema_context(self, data: dict):
        for name, definition in data.items():
            self.__attributes[name] = definition

        return self

    def get_attribute_definition(self, attribute_name):
        return self.__attributes.get(attribute_name, None)
