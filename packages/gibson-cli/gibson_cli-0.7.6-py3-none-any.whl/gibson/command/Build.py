import sys

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.db.TableExceptions import TableExceptions


class Build(BaseCommand):
    def __build_datastore(self):
        self.configuration.display_project()

        db = create_engine(self.configuration.project.datastore.uri)
        session = sessionmaker(autocommit=False, autoflush=False, bind=db)()
        table_exceptions = TableExceptions().universal()

        self.conversation.type("Connected to datastore...\n")

        if self.configuration.project.datastore.type == "mysql":
            self.__build_mysql(session)
        elif self.configuration.project.datastore.type == "postgresql":
            self.__build_postgresql(session)

        self.conversation.newline()

    def __build_mysql(self, session):
        try:
            table_exceptions = TableExceptions().mysql()

            session.execute("set foreign_key_checks = 0")
            self.conversation.type("  foreign key checks have been disabled\n")

            tables = session.execute("show tables").all()
            if len(tables) > 0:
                self.conversation.type("  dropping existing entities\n")

                for table in tables:
                    if table not in table_exceptions:
                        self.conversation.type(f"    {table[0]}\n")
                        session.execute(f"drop table if exists {table[0]}")

            self.conversation.type("  building entities\n")

            for entity in self.memory.entities:
                self.conversation.type(f"    {entity['name']}\n")
                session.execute(entity["definition"])
        finally:
            session.execute("set foreign_key_checks = 1")
            self.conversation.type("  foreign key checks have been enabled\n")

    def __build_postgresql(self, session):
        table_exceptions = TableExceptions().postgresql()

        schema = list(session.execute("select current_schema()"))[0][0]
        self.conversation.type(f"  current schema is {schema}\n")

        tables = list(
            session.execute(
                """select table_name
                     from information_schema.tables
                    where table_schema = :table_schema and table_type = 'BASE TABLE'""",
                {"table_schema": schema},
            )
        )

        if len(tables) > 0:
            self.conversation.type("  dropping existing entities\n")

            for table in tables:
                self.conversation.type(f"    {table[0]}\n")
                session.execute(f"drop table if exists {schema}.{table[0]} cascade")
                session.commit()

        self.conversation.type("  building entities\n")

        tables = {}
        for entity in self.memory.entities:
            tables[entity["name"]] = entity["definition"]

        while tables != {}:
            remove = []
            for name, definition in tables.items():

                try:
                    session.execute(definition)
                    session.commit()

                    self.conversation.type(f'    {name.split(".")[-1]}\n')

                    remove.append(name)
                except sqlalchemy.exc.ProgrammingError:
                    session.rollback()

            for name in remove:
                del tables[name]

    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] != "datastore":
            self.usage()

        self.configuration.require_project()

        if self.memory.entities is None or len(self.memory.entities) == 0:
            self.no_entities()

        self.__build_datastore()

    def no_entities(self):
        self.configuration.display_project()
        self.conversation.type(
            "Ahhh man. I would love to but there aren't any entities.\n"
        )
        self.conversation.newline()
        exit(1)

    def usage(self):
        self.configuration.display_project()
        datastore_uri = (
            self.configuration.project.datastore.uri
            if self.configuration.project
            else ""
        )
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'build', args='datastore', hint='build the datastore')} {datastore_uri}\n"
        )
        self.conversation.newline()
        exit(1)
