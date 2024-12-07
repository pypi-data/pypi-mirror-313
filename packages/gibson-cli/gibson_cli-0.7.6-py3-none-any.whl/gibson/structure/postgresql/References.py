class References:
    def __init__(self):
        self.columns = []
        self.match_full = None
        self.match_partial = None
        self.match_simple = None
        self.on_delete = None
        self.on_update = None
        self.ref_schema = None
        self.ref_table = None

    def json(self):
        return {
            "attributes": self.columns,
            "datastore": {
                "specifics": {
                    "match": {
                        "full": self.match_full,
                        "partial": self.match_partial,
                        "simple": self.match_simple,
                    },
                }
            },
            "entity": {"name": self.ref_table, "schema_": self.ref_schema},
            "on": {"delete": self.on_delete, "update": self.on_update},
            "sql": self.sql(),
        }

    def sql(self):
        parts = []

        ref_table = []
        if self.ref_schema is not None:
            ref_table.append(self.ref_schema)
        ref_table.append(self.ref_table)

        if self.ref_table is not None:
            parts.append(".".join(ref_table))

        if self.columns != []:
            parts.append("(" + ", ".join(self.columns) + ")")

        if self.match_full is True:
            parts.append("match full")

        if self.match_partial is True:
            parts.append("match partial")

        if self.match_simple is True:
            parts.append("match simple")

        if self.on_delete is not None:
            parts.append(f"on delete {self.on_delete}")

        if self.on_update is not None:
            parts.append(f"on update {self.on_update}")

        if parts == []:
            return ""

        return ("references " + " ".join(parts)).lstrip().rstrip()
