import sys

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.rewrite.Rewrite import Rewrite


class Entity(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        self.configuration.display_project()

        if self.memory.recall_entity(sys.argv[3]) is None:
            self.conversation.type(
                f'Nothing renamed, did not find entity named "{sys.argv[3]}".\n'
            )
            self.conversation.newline()
            return self

        if self.memory.recall_entity(sys.argv[4]) is not None:
            self.conversation.type(
                f'Cannot rename to "{sys.argv[4]}" because that entity already exists.\n'
            )
            self.conversation.newline()
            return self

        cli = Cli(self.configuration)

        last = self.memory.recall_last()
        if last is not None:
            response = cli.modeler_entity_rename(
                self.configuration.project.modeler.version,
                last["entities"],
                sys.argv[3],
                sys.argv[4],
            )

            self.memory.remember_last({"entities": response["entities"]})

        stored = self.memory.recall_entities()
        if stored is not None:
            response = cli.modeler_entity_rename(
                self.configuration.project.modeler.version,
                stored,
                sys.argv[3],
                sys.argv[4],
            )

            self.memory.remember_entities(response["entities"])

        self.conversation.type(f"[Renamed] {sys.argv[3]} -> {sys.argv[4]}\n")
        self.conversation.newline()

        Rewrite(self.configuration, header="Refactoring").write()

        self.conversation.newline()

        return self
