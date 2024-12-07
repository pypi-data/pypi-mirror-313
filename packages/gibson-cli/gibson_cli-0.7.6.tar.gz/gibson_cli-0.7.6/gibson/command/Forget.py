import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand


class Forget(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] not in ["all", "last", "stored"]:
            self.usage()

        self.configuration.require_project()
        self.configuration.display_project()

        if sys.argv[2] in ["all", "last"]:
            self.memory.forget_last()
            self.conversation.type(f"last memory is forgotten.\n")

        if sys.argv[2] in ["all", "stored"]:
            self.memory.forget_entities()
            self.conversation.type(f"stored memory is forgotten.\n")

        self.conversation.newline()

        return self

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'forget', args=['all', 'last', 'stored'], hint='delete entities from memory')}\n"
        )
        self.conversation.newline()
        exit(1)
