import os
import shutil
import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Api import Api
from gibson.command.code.Base import Base
from gibson.command.code.Models import Models
from gibson.command.code.Schemas import Schemas
from gibson.command.code.Tests import Tests
from gibson.core.Configuration import Configuration
from gibson.core.TimeKeeper import TimeKeeper
from gibson.services.code.customization.CustomizationManager import CustomizationManager


class Rewrite(BaseCommand):
    def __init__(
        self,
        configuration: Configuration,
        header="Writing Code",
        wipe=True,
        with_header=False,
    ):
        super().__init__(configuration)
        self.wipe = wipe
        self.with_header = with_header

    def execute(self):
        if len(sys.argv) == 2:
            self.write()
        else:
            self.usage()

    def write(self, argument=None):
        self.configuration.require_project()
        self.configuration.require_project_key()

        if len(self.memory.recall_merged()) == 0:
            self.conversation.cant_no_entities(self.configuration.project.name)
            exit(1)

        if self.with_header is True:
            self.configuration.display_project()

        customization_manager = CustomizationManager(self.configuration).preserve()

        try:
            if argument is None and self.wipe is True:
                for root, dirs, files in os.walk(
                    os.path.expandvars(self.configuration.project.dev.base.path)
                ):
                    for file in files:
                        os.unlink(os.path.join(root, file))

                    for dir_ in dirs:
                        shutil.rmtree(os.path.join(root, dir_))

            self.conversation.type("Writing Code\n")

            if argument is None or argument == "api":
                time_keeper = TimeKeeper()
                self.conversation.type("  API      ")
                self.conversation.mute()
                # Disable customization management here so we don't process this
                # twice (see finally block).
                Api(self.configuration).disable_customization_management().execute()
                self.conversation.unmute()
                self.conversation.type(time_keeper.get_display())
                self.conversation.newline()

            if argument is None or argument == "base":
                time_keeper = TimeKeeper()
                self.conversation.type("  Base     ")
                self.conversation.mute()
                Base(self.configuration).execute()
                self.conversation.unmute()
                self.conversation.type(time_keeper.get_display())
                self.conversation.newline()

            if argument is None or argument == "models":
                time_keeper = TimeKeeper()
                self.conversation.type("  Models   ")
                self.conversation.mute()
                Models(self.configuration).execute()
                self.conversation.unmute()
                self.conversation.type(time_keeper.get_display())
                self.conversation.newline()

            if argument is None or argument == "schemas":
                time_keeper = TimeKeeper()
                self.conversation.type("  Schemas  ")
                self.conversation.mute()
                Schemas(self.configuration).execute()
                self.conversation.unmute()
                self.conversation.type(time_keeper.get_display())
                self.conversation.newline()

            if argument is None or argument == "tests":
                time_keeper = TimeKeeper()
                self.conversation.type("  Tests    ")
                self.conversation.mute()
                Tests(self.configuration).execute()
                self.conversation.unmute()
                self.conversation.type(time_keeper.get_display())
                self.conversation.newline()
        finally:
            customization_manager.restore()

        if self.with_header is True:
            self.conversation.newline()

        return self

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'rewrite', hint='rewrite all code')}\n"
        )
        self.conversation.newline()
        exit(1)
