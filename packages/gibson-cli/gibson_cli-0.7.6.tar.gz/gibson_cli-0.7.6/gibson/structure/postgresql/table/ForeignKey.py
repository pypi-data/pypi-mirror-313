class ForeignKey:
    def __init__(self):
        self.columns = []
        self.references = None
        self.relationship = None

    def json(self):
        return {
            "attributes": self.columns,
            "references": self.references.json()
            if self.references is not None
            else None,
            "sql": self.sql(),
        }

    def sql(self):
        parts = []

        if self.columns != []:
            parts.append("(" + ", ".join(self.columns) + ")")

        if self.references is not None:
            parts.append(self.references.sql())

        if parts == []:
            return ""

        return ("foreign key " + " ".join(parts)).lstrip().rstrip()
