import requests

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.conf.Version import Version as VersionConf


class Version(BaseCommand):
    def execute(self):
        try:
            r = requests.get("https://pypi.org/pypi/gibson-cli/json")
            latest_version = r.json()["info"]["version"]
        except:
            latest_version = VersionConf.num

        if latest_version != VersionConf.num:
            self.conversation.type(
                f"A new version of {Colors.command(self.configuration.command)} is available: {Colors.cyan(latest_version)}\n"
            )
            self.conversation.type(
                f"You are currently using version: {Colors.violet(VersionConf.num)}\n"
            )
            self.conversation.type(
                f"Please update to the latest version by running: {Colors.command('pip3', 'install', args='--upgrade', inputs='gibson-cli')}\n"
            )
        else:
            self.conversation.type(
                f"Nice! 🎉 You are using the latest version of {Colors.command(self.configuration.command)}: {Colors.cyan(VersionConf.num)}\n"
            )
