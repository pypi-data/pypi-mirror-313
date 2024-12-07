class ReferenceConstraint:
    def __init__(self):
        self.attributes = None
        self.match = None
        self.on_delete = None
        self.on_update = None
        self.references = None

    def json(self):
        return {
            "attributes": self.attributes,
            "datastore": {
                "specifics": {
                    "match": self.match,
                }
            },
            "entity": {"name": self.references, "schema_": None},
            "on": {"delete": self.on_delete, "update": self.on_update},
            "sql": self.sql(),
        }

    def sql(self):
        if self.attributes is None or self.attributes == []:
            raise RuntimeError("reference constraint is missing attributes")

        if self.references is None:
            raise RuntimeError("reference constraint is missing referenced entity")

        parts = ["references", self.references, "(" + ", ".join(self.attributes) + ")"]

        if self.match is not None:
            parts.append(f"match {self.match}")

        if self.on_delete is not None:
            parts.append(f"on delete {self.on_delete}")

        if self.on_update is not None:
            parts.append(f"on update {self.on_update}")

        return " ".join(parts)
