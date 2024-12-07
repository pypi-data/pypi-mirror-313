import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Spinner import Spinner
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Model(BaseCommand):
    def execute(self, entity_name=None):
        entity_name = entity_name or sys.argv[3]
        self.configuration.require_project()
        entity = self.memory.recall_stored_entity(entity_name)
        if entity is None:
            self.conversation.not_sure_no_entity(self.configuration, entity_name)
            exit(1)

        time_keeper = TimeKeeper()

        with Spinner("Gibson is writing the model...", "Model written"):
            cli = Cli(self.configuration)
            response = cli.code_models([entity["name"]])
            Dev(self.configuration).model(
                response["code"][0]["entity"]["name"], response["code"][0]["definition"]
            )

        if self.configuration.project.dev.active is True:
            self.conversation.type(
                f"\nGibson wrote the following {Colors.argument('model')} code to your project:\n"
            )

        if not self.conversation.muted():
            print(response["code"][0]["definition"])
            time_keeper.display()
