import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.rename.Entity import Entity


class Rename(BaseCommand):
    def execute(self):
        if len(sys.argv) == 5 and sys.argv[2] == "entity":
            Entity(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'rename', args='entity', inputs=['[existing name]', '[new name]'], hint='rename an entity')}\n"
        )
        self.conversation.newline()
        exit(1)
