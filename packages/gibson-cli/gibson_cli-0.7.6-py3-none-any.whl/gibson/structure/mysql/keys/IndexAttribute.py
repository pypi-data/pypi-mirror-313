class IndexAttribute:
    def __init__(self):
        self.asc = None
        self.desc = None
        self.name = None

    def sql(self):
        sql = self.name
        if self.asc is True:
            sql += " asc"
        elif self.desc is True:
            sql += " desc"

        return sql
