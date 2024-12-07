from gibson.structure.mysql.keys.IndexAttribute import IndexAttribute


class Index:
    def __init__(self):
        self.__attribute_name_list = []
        self.attributes = None
        self.name = None
        self.using = None

    def add_attribute(self, name, asc=False, desc=False):
        if asc is True and desc is True:
            raise RuntimeError("an index attribute cannot be both asc and desc")

        if self.attributes is None:
            self.attributes = []

        attribute = IndexAttribute()
        attribute.name = name

        if asc is True:
            attribute.asc = True
        elif desc is True:
            attribute.desc = True

        self.attributes.append(attribute)
        self.__attribute_name_list.append(name)

        return self

    def attribute_name_list(self):
        return self.__attribute_name_list

    def json(self):
        return {
            "attributes": self.__attribute_name_list,
            "datastore": {
                "specifics": {
                    "name": self.name,
                    "using": self.using,
                }
            },
            "sql": self.sql(),
        }

    def reset_attributes(self):
        self.__attribute_name_list = []
        self.attributes = None
        return self

    def sql(self):
        if self.attributes is None or self.attributes == []:
            raise RuntimeError("index is missing attributes")

        parts = ["index"]
        if self.name is not None:
            parts.append(self.name)

        if self.using is not None:
            parts.append(f"using {self.using}")

        attributes = []
        for attribute in self.attributes:
            attributes.append(attribute.sql())

        parts.append("(" + ", ".join(attributes) + ")")

        return " ".join(parts)
