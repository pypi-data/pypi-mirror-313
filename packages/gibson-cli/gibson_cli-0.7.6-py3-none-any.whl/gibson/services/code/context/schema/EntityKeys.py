from gibson.structure.mysql.constraints.ReferenceConstraint import ReferenceConstraint
from gibson.structure.mysql.keys.ForeignKey import ForeignKey
from gibson.structure.mysql.keys.Index import Index


class EntityKeys:
    def __init__(self):
        self.__entity_name = None
        self.__index = []
        self.__primary = []
        self.__unique = []

    def best_sql_foreign_key(self):
        elements = []
        if self.__primary != []:
            elements = self.__primary
        elif self.__unique != []:
            elements = self.__unique

        if elements == []:
            return None

        reference_constraint = ReferenceConstraint()
        reference_constraint.attributes = []
        reference_constraint.references = self.__entity_name

        foreign_key = ForeignKey()
        foreign_key.attributes = []
        foreign_key.reference = reference_constraint

        index = Index()

        data_types = []
        for element in elements:
            foreign_key.attributes.append(f"{self.__entity_name}_{element['name']}")
            reference_constraint.attributes.append(element["name"])
            index.add_attribute(f"{self.__entity_name}_{element['name']}")
            data_types.append(element["data"]["type"])

        return foreign_key, index, data_types

    def from_code_writer_schema_context(
        self, entity_name: str, index: list, primary: list, unique: list
    ):
        self.__entity_name = entity_name
        self.__index = index
        self.__primary = primary
        self.__unique = unique
        return self
