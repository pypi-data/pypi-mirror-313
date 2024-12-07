class TableExceptions:
    def mysql(self):
        return self.universal()

    def postgresql(self):
        return self.universal()

    def universal(self):
        return ["alembic_version"]
