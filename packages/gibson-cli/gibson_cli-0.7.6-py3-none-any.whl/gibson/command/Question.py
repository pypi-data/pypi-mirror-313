import os
import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand


class Question(BaseCommand):
    TOKEN_FILE = "file://"
    TOKEN_PYTHON = "py://"
    TOKEN_SQL = "sql://"

    def execute(self):
        if len(sys.argv) < 3:
            self.usage()

        self.configuration.require_project()
        instructions = ""
        has_file = False
        has_python = False
        has_sql = False
        for term in sys.argv[2:]:
            if self.TOKEN_FILE in term:
                token, path = term.split(self.TOKEN_FILE)

                try:
                    with open(path, "r") as f:
                        contents = f.read()
                except FileNotFoundError:
                    self.configuration.display_project()
                    self.conversation.file_not_found(path)
                    self.conversation.newline()
                    exit(1)

                has_file = True
                instructions += f"\n\n{contents}\n\n"
            elif self.TOKEN_PYTHON in term:
                token, import_ = term.split(self.TOKEN_PYTHON)
                import_ = import_.replace(".", "/")

                contents = None
                for path in os.environ["PYTHONPATH"].split(":"):
                    try:
                        with open(f"{path}/{import_}.py", "r") as f:
                            contents = f.read()
                    except FileNotFoundError:
                        pass

                if contents is None:
                    self.__python_import_not_found(import_.replace("/", "."))

                has_python = True
                instructions += f"\n\n{contents}\n\n"
            elif self.TOKEN_SQL in term:
                token, name = term.split(self.TOKEN_SQL)

                entity = self.memory.recall_entity(name)
                if entity is None:
                    self.conversation.not_sure_no_entity(self.configuration, name)
                    exit(1)

                has_sql = True
                instructions += f"\n\n{entity['definition']}\n\n"
            else:
                instructions += f"{term} "

        if instructions != "":
            cli = Cli(self.configuration)
            response = cli.llm_query(instructions, has_file, has_python, has_sql)

        if response["entities"] is not None and len(response["entities"]) > 0:
            self.memory.remember_last({"entities": response["entities"]})

        self.conversation.raw_llm_response()
        print(response["commentary"].rstrip())

        if response["entities"] is not None and len(response["entities"]) > 0:
            self.conversation.newline()
            self.conversation.entities_hijacked()
            self.conversation.newline()

        self.conversation.newline()

    def __python_import_not_found(self, import_):
        self.configuration.display_project()
        self.conversation.type(f'That\'s a misfire, "{import_}" does not exist.\n')
        self.conversation.newline()
        exit(1)

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'q', inputs='[instructions]', hint='ask a question or tell Gibson to do something using natural language')}\n"
        )
        self.conversation.type(
            f"    use {Colors.argument(self.TOKEN_FILE+'[path]')} to import a file from the filesystem\n"
        )
        self.conversation.type(
            f"    use {Colors.argument(self.TOKEN_PYTHON+'[import]')} to import a file from PYTHONPATH\n"
        )
        self.conversation.type(
            f"    use {Colors.argument(self.TOKEN_SQL+'[entity name]')} to import SQL\n"
        )

        self.conversation.newline()
        exit(1)
