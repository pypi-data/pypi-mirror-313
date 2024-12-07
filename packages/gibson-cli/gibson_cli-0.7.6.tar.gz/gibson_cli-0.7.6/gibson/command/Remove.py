import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.rewrite.Rewrite import Rewrite


class Remove(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        self.configuration.require_project()
        self.configuration.display_project()

        found = False

        last = self.memory.recall_last()
        if last is not None:
            entities = []
            for entity in last["entities"]:
                if entity["name"] == sys.argv[2]:
                    found = True
                else:
                    entities.append(entity)

            if found:
                if len(entities) == 0:
                    self.memory.forget_last()
                else:
                    self.memory.remember_last({"entities": entities})

                self.conversation.type(
                    f"[Removed] {sys.argv[2]} from {Colors.argument('last')} memory\n"
                )
                self.conversation.newline()

                return self

        cli = Cli(self.configuration)
        entities = []

        stored = self.memory.recall_entities()
        if stored is not None and len(stored) > 0:
            for entity in stored:
                entities.append(entity)
                if entity["name"] == sys.argv[2]:
                    found = True

        if not found:
            self.conversation.type(
                f"Nothing removed, no entity named {Colors.entity(sys.argv[2])}.\n"
            )
            self.conversation.newline()
            return self

        response = cli.modeler_entity_remove(
            self.configuration.project.modeler.version, entities, sys.argv[2]
        )

        if len(response["entities"]) == 0:
            self.memory.forget_entities()
        else:
            self.memory.remember_entities(response["entities"])

        self.conversation.type(f"[Removed] {sys.argv[2]}\n")
        self.conversation.newline()

        Rewrite(self.configuration, header="Refactoring").write()

        self.conversation.newline()

        return self

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'remove', inputs='[entity name]', hint='remove an entity from the project')}\n"
        )
        self.conversation.newline()
        exit(1)
