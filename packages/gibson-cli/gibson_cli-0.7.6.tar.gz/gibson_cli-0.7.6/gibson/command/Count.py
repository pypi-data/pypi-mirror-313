import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand


class Count(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] not in ["last", "stored"]:
            self.usage()

        self.configuration.require_project()

        if sys.argv[2] == "last":
            count = 0
            if self.memory.last is not None:
                count = len(self.memory.last["entities"])

            print(count)
        elif sys.argv[2] == "stored":
            count = 0
            if self.memory.entities is not None:
                count = len(self.memory.entities)

            print(count)
        else:
            raise NotImplementedError

        return self

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'count', args=['last', 'stored'], hint='display the number of entities')}\n"
        )
        self.conversation.newline()
        exit(1)
