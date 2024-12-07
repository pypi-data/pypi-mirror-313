import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Entity import Entity as CodeEntity
from gibson.command.new.Module import Module as NewModule
from gibson.command.new.Project import Project as NewProject


class New(BaseCommand):
    def execute(self):
        if len(sys.argv) == 3 and sys.argv[2] == "project":
            NewProject(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "module":
            NewModule(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "entity":
            CodeEntity(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'new', args=['project', 'module', 'entity'], hint='create something new')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'new', args='project', hint='create a new project')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'new', args='module', hint='create a new module')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'new', args='entity', inputs='[entity name]', hint='create a new entity')}\n"
        )
        self.conversation.newline()
        exit(1)
