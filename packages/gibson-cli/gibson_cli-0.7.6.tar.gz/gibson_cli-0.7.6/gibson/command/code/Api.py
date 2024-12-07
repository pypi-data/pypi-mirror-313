from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev
from gibson.services.code.customization.Authenticator import Authenticator


class Api(BaseCommand):
    def execute(self):
        time_keeper = TimeKeeper()
        dev = Dev(self.configuration)

        cli = Cli(self.configuration)
        response = cli.code_api()

        if self.customization_management_is_enabled() is True:
            authenticator = Authenticator(self.configuration).preserve()

        try:
            for entry in response["code"]:
                dev.api_component(entry["name"], entry["definition"])

                if self.conversation.muted() is False:
                    print(entry["definition"])
        finally:
            if self.customization_management_is_enabled() is True:
                authenticator.restore()

        if self.conversation.muted() is False:
            time_keeper.display()
