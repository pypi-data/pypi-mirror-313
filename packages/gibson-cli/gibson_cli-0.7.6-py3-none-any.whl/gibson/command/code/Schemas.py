from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Schemas(BaseCommand):
    def execute(self):
        entities = []
        if self.memory.entities is not None:
            for entity in self.memory.entities:
                entities.append(entity["name"])

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_schemas(entities)

        for entry in response["code"]:
            Dev(self.configuration).schema(entry["entity"]["name"], entry["definition"])

            if self.conversation.muted() is False:
                print(entry["definition"])

        if self.conversation.muted() is False:
            time_keeper.display()
