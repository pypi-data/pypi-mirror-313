from gibson.services.code.context.schema.DataDictionary import DataDictionary
from gibson.services.code.context.schema.EntityKeys import EntityKeys


class Manager:
    def __init__(self):
        self.__entity_keys_map = {}
        self.data_dictionary = DataDictionary()
        self.json = None

    def from_code_writer_schema_context(self, context: dict):
        self.data_dictionary.from_code_writer_schema_context(
            context["data"]["dictionary"]
        )

        for entity_name, keys in context["keys"].items():
            self.__entity_keys_map[
                entity_name
            ] = EntityKeys().from_code_writer_schema_context(
                entity_name, keys["index"], keys["primary"], keys["unique"]
            )

        self.json = context

        return self

    def get_entity_keys(self, entity_name):
        return self.__entity_keys_map.get(entity_name, None)
