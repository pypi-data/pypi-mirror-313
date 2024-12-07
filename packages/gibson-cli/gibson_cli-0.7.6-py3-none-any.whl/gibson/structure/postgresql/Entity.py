from gibson.structure.postgresql.table.ForeignKey import ForeignKey


class Entity:
    def __init__(self):
        self.attributes = None
        self.constraints = None
        self.keys = None
        self.name = None
        self.table = None

    def add_attribute(self, name, data_type, after=None, before=None):
        was_added = False

        json = {
            "check": None,
            "datastore": {
                "specifics": {
                    "references": None,
                }
            },
            "data_type": {
                "formatted": data_type,
                "raw": data_type,
            },
            "default": None,
            "key": {"index": None, "primary": None, "unique": None},
            "length": None,
            "name": name,
            "nullable": None,
            "numeric": {
                "precision": None,
                "scale": None,
            },
            "sql": f"{name} {data_type}",
        }

        attributes = []
        for attribute in self.attributes:
            if was_added is False and attribute["name"] == after:
                was_added = True
                attributes.append(attribute)
                attributes.append(json)
            elif was_added is False and attribute["name"] == before:
                was_added = True
                attributes.append(json)
                attributes.append(attribute)
            else:
                attributes.append(attribute)

        if was_added is False:
            attributes.append(json)

        self.attributes = attributes
        return self

    def add_foreign_key(self, foreign_key: ForeignKey):
        self.keys["foreign"].append(foreign_key.json())
        return self

    def add_index(self, index: object):
        return self

    def create_statement(self):
        parts = []
        for attribute in self.attributes:
            parts.append("    " + attribute["sql"])

        if self.keys["primary"] is not None:
            parts.append("    " + self.keys["primary"]["sql"])

        for unique_key in self.keys["unique"]:
            parts.append("    " + unique_key["sql"])

        for index in self.keys["index"]:
            parts.append("    " + index["sql"])

        for fk in self.keys["foreign"]:
            parts.append("    " + fk["sql"])

        for check in self.constraints["check"]:
            parts.append("    " + check["sql"])

        parameters = ""
        if self.table["parameters"] and self.table["parameters"].get("sql"):
            parameters = " " + self.table["parameters"].get("sql")

        return (
            f"create table if not exists {self.name}(\n"
            + ",\n".join(parts)
            + f"\n){parameters}"
        )

    def import_from_struct(self, data: dict):
        if "name" in data and "struct" in data:
            self.name = data["name"]

            for key in data["struct"].keys():
                setattr(self, key, data["struct"][key])
        elif "entity" in data and "struct" in data["entity"]:
            self.name = data["entity"]["name"]

            for key in data["entity"]["struct"].keys():
                setattr(self, key, data["entity"]["struct"][key])
        else:
            raise RuntimeError("cannot import from struct, incorrect data format")

        return self
