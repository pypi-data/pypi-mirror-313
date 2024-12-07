import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Api import Api as CodeApi
from gibson.command.code.Base import Base as CodeBase
from gibson.command.code.Entity import Entity as CodeEntity
from gibson.command.code.Model import Model as CodeModel
from gibson.command.code.Models import Models as CodeModels
from gibson.command.code.Schema import Schema as CodeSchema
from gibson.command.code.Schemas import Schemas as CodeSchemas
from gibson.command.code.Test import Test as CodeTest
from gibson.command.code.Tests import Tests as CodeTests


class Code(BaseCommand):
    def execute(self):
        if len(sys.argv) == 3 and sys.argv[2] == "api":
            CodeApi(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "base":
            CodeBase(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "entity":
            CodeEntity(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "models":
            CodeModels(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "models":
            CodeModel(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "schemas":
            CodeSchemas(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "schemas":
            CodeSchema(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "tests":
            CodeTests(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "tests":
            CodeTest(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'code', args=['api', 'base', 'entity', 'models', 'schemas', 'tests'], inputs='[entity name]', hint='write code')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='api', hint='generate the API code')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='base', hint='generate the base code')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='entity', inputs='[entity name]', hint='create or update an entity using the AI pair programmer')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='models', hint='generate the models for all entities')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='models', inputs='[entity name]', hint='generate the model(s) for a single entity')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='schemas', hint='generate the schemas for all entities')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='schemas', inputs='[entity name]', hint='generate the schema(s) for a single entity')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='tests', hint='generate the unit tests for all entities')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'code', args='tests', inputs='[entity name]', hint='generate the unit tests for a single entity')}\n"
        )
        self.conversation.newline()
        exit(1)
