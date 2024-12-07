import re
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.importer.OpenApi import OpenApi
from gibson.command.rewrite.Rewrite import Rewrite
from gibson.db.TableExceptions import TableExceptions


class Import(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        write_code = False

        if len(sys.argv) == 3 and sys.argv[2] == "api":
            entities = self.__import_from_api()
            write_code = self.configuration.project.dev.active
        elif len(sys.argv) == 3 and sys.argv[2] == "mysql":
            entities = self.__import_from_mysql()
            write_code = self.configuration.project.dev.active
        elif len(sys.argv) == 4 and sys.argv[2] == "pg_dump":
            entities = self.__import_from_postgresql()
            write_code = self.configuration.project.dev.active
        elif len(sys.argv) == 4 and sys.argv[2] == "openapi":
            return OpenApi(self.configuration).execute()
        else:
            self.usage()

        self.memory.remember_entities(entities)

        word_entities = "entity" if len(entities) == 1 else "entities"

        if len(entities) > 0:
            self.conversation.newline()

        self.conversation.type("Summary\n")
        self.conversation.type(f"    {len(entities)} {word_entities} imported\n")
        self.conversation.newline()

        if write_code:
            Rewrite(self.configuration).write()
            self.conversation.newline()

        return True

    def __import_from_api(self):
        self.configuration.display_project()

        self.conversation.type("Connected to API...\n")
        response = Cli(self.configuration).import_()
        self.conversation.type("Building schema...\n")

        for entity in response["project"]["entities"]:
            self.conversation.type(f"    {entity['name']}\n")

        return response["project"]["entities"]

    def __import_from_mysql(self):
        db = create_engine(self.configuration.project.datastore.uri)
        session = sessionmaker(autocommit=False, autoflush=False, bind=db)()

        table_exceptions = TableExceptions().mysql()

        self.conversation.type("Connected to datastore...\n")
        self.conversation.type("Building schema...\n")

        tables = session.execute("show tables").all()

        entities = []
        for table in tables:
            if table[0] not in table_exceptions:
                self.conversation.type(f"    {table[0]}\n")

                create_statement = session.execute(
                    f"show create table {table[0]}"
                ).one()

                entities.append(
                    {"definition": str(create_statement[1]), "name": str(table[0])}
                )

        return entities

    def __import_from_postgresql(self):
        self.conversation.type("Reading pg_dump file...\n")

        try:
            with open(sys.argv[3], "r") as f:
                contents = f.read()
        except FileNotFoundError:
            self.conversation.file_not_found(sys.argv[3])
            self.conversation.newline()
            exit(1)

        lines = contents.split("\n")

        tables = {}
        for i in range(len(lines)):
            matches = re.search(
                r"^create table (.*)\s+\(", lines[i].lstrip().rstrip(), re.IGNORECASE
            )
            if matches:
                table_name = matches[1].split(".")[-1]
                definition = []

                while True:
                    i += 1

                    if lines[i].lstrip().rstrip() == ");":
                        tables[table_name] = definition
                        break
                    else:
                        definition.append(lines[i].lstrip().rstrip())
            else:
                matches = re.search(
                    r"^alter table(?:\s+only)\s+(.*)$",
                    lines[i].lstrip().rstrip(),
                    re.IGNORECASE,
                )
                if matches:
                    table_name = matches[1].split(".")[-1]

                    i += 1
                    matches = re.search(
                        r"^add (constraint .*?);?$",
                        lines[i].lstrip().rstrip(),
                        re.IGNORECASE,
                    )
                    if matches:
                        if tables[table_name][-1][-1] != ",":
                            tables[table_name][-1] += ","

                        tables[table_name].append(matches[1] + ",")

        entities = []
        for table_name, definition in tables.items():
            self.conversation.type(f"    {table_name}\n")

            definition[-1] = definition[-1].rstrip(",")

            create_table = f"create table if not exists {table_name} (\n"
            for entry in definition:
                create_table += " " * 4 + entry + "\n"
            create_table += ")"

            entities.append({"definition": create_table, "name": table_name})

        return entities

    def usage(self):
        self.configuration.display_project()
        datastore_uri = (
            self.configuration.project.datastore.uri
            if self.configuration.project
            else ""
        )
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'import', args=['api', 'mysql', 'pg_dump', 'openapi'], hint='import entities')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'import', args='api', hint=f'import all entities from your project created on {Colors.link(self.configuration.app_domain())}')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'import', args='mysql', hint='import all entities from your MySQL database')} ({Colors.link(datastore_uri)})\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'import', args='pg_dump', inputs='path/to/pg_dump.sql', hint='import all entities from a pg_dump file')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'import', args='openapi', inputs='path/to/openapi.json', hint='import all entities from an OpenAPI spec file')}\n"
        )
        self.conversation.newline()
        exit(1)
