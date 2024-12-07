import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand


class Show(BaseCommand):
    def execute(self):
        if len(sys.argv) == 2:
            self.configuration.require_project()
            entities = self.memory.recall_merged()
            if entities is None:
                self.conversation.cant_no_entities(self.configuration.project.name)
                exit(1)
        elif len(sys.argv) == 3:
            self.configuration.require_project()
            entity = self.memory.recall_entity(sys.argv[2])
            if entity is None:
                self.conversation.not_sure_no_entity(self.configuration, sys.argv[2])
                exit(1)

            entities = [entity]
        else:
            self.usage()

        for entity in sorted(entities, key=lambda x: x["name"]):
            statement = Colors.table(entity["definition"], entity["name"])
            print(f"\n{statement}")

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'show', hint='display the entire schema')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'show', inputs='[entity name]', hint='display the schema for an entity')}\n"
        )
        self.conversation.newline()
        exit(1)
