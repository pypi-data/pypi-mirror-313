from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Base(BaseCommand):
    def execute(self):
        time_keeper = TimeKeeper()
        dev = Dev(self.configuration)

        cli = Cli(self.configuration)
        response = cli.code_base()

        for entry in response["code"]:
            dev.base_component(entry["name"], entry["definition"])

            if self.conversation.muted() is False:
                print(entry["definition"])

        if self.conversation.muted() is False:
            time_keeper.display()
