import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Spinner import Spinner
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Schema(BaseCommand):
    def execute(self, entity_name=None):
        entity_name = entity_name or sys.argv[3]
        self.configuration.require_project()
        entity = self.memory.recall_stored_entity(entity_name)
        if entity is None:
            self.conversation.not_sure_no_entity(self.configuration, entity_name)
            exit(1)

        time_keeper = TimeKeeper()

        with Spinner("Gibson is writing the schemas...", "Schemas written"):
            cli = Cli(self.configuration)
            response = cli.code_schemas([entity["name"]])
            code = response["code"][0] if len(response["code"]) > 0 else None
            if code:
                Dev(self.configuration).schema(
                    code["entity"]["name"], code["definition"]
                )

        if code and self.configuration.project.dev.active is True:
            self.conversation.type(
                f"\nGibson wrote the following {Colors.argument('schema')} code to your project:\n"
            )

        if not self.conversation.muted():
            if code:
                print(code["definition"])
            time_keeper.display()
