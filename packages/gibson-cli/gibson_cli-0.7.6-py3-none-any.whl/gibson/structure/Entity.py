from gibson.structure.mysql.Entity import Entity as MysqlEntity
from gibson.structure.postgresql.Entity import Entity as PostgresqlEntity


class Entity:
    TYPE_MYSQL = "mysql"
    TYPE_POSTGRESQL = "postgresql"

    def instantiate(self, datastore_type: str):
        if datastore_type not in [self.TYPE_MYSQL, self.TYPE_POSTGRESQL]:
            raise RuntimeError(f'unrecognized datastore type "{datastore_type}"')

        if datastore_type == self.TYPE_MYSQL:
            return MysqlEntity()
        elif datastore_type == self.TYPE_POSTGRESQL:
            return PostgresqlEntity()

        raise NotImplementedError(f'"{datastore_type}" is not currently supported')
