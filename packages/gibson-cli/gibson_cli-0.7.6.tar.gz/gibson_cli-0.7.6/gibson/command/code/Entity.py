from __future__ import annotations

import os
import sys
from string import Template

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Base import Base
from gibson.command.code.Model import Model
from gibson.command.code.Schema import Schema
from gibson.command.code.Test import Test
from gibson.command.Merge import Merge
from gibson.core.Configuration import Configuration
from gibson.core.Diff import additions, diff
from gibson.core.Spinner import ComputingSpinner, Spinner
from gibson.display.Header import Header
from gibson.display.WorkspaceFooter import WorkspaceFooter
from gibson.display.WorkspaceHeader import WorkspaceHeader
from gibson.services.code.context.schema.Manager import (
    Manager as CodeContextSchemaManager,
)
from gibson.structure.Entity import Entity as StructureEntity


class Entity(BaseCommand):
    CODE_WRITER_ENTITY_MODIFIER_NOOP = ""

    def __init__(self, configuration: Configuration):
        super().__init__(configuration)
        self.__context = None

    def __add_foreign_key(self, entity, entity_name):
        entity_keys = self.__context.get_entity_keys(entity_name)
        if entity_keys is None:
            self.conversation.type(
                f'\nThe entity you referenced, "{entity_name}", does not exist.\n'
            )
            self.conversation.wait()
            return False

        best_sql_foreign_key = entity_keys.best_sql_foreign_key()
        if best_sql_foreign_key is None:
            self.conversation.type(
                f'\nYou cannot make a foreign key to "{entity_name}".\n'
                + "It does not have primary or unique keys.\n"
            )
            self.conversation.wait()
            return False

        foreign_key, index, data_types = best_sql_foreign_key

        for i in range(len(foreign_key.attributes)):
            entity.add_attribute(
                foreign_key.attributes[i],
                data_types[i],
                after="uuid",
                before="date_created",
            )

        entity.add_foreign_key(foreign_key)
        entity.add_index(index)

        return True

    def execute(self):
        cli = Cli(self.configuration)
        entity_name = sys.argv[3]
        existing_entity = self.memory.recall_entity(entity_name)
        definition = (
            existing_entity["definition"]
            if existing_entity
            else self.template_definition(entity_name)
        )

        with ComputingSpinner():
            self.__context = CodeContextSchemaManager().from_code_writer_schema_context(
                cli.code_writer_schema_context()
            )
            data = cli.code_writer_entity_modifier(
                self.__context.json,
                sys.argv[3],
                definition,
                self.CODE_WRITER_ENTITY_MODIFIER_NOOP,
            )
            entity = (
                StructureEntity()
                .instantiate(self.configuration.project.datastore.type)
                .import_from_struct(data)
            )
            original_entity = entity if existing_entity else None
            original_model_code = (
                data["code"][0]["definition"] if existing_entity else None
            )

        while True:
            try:
                self.__render_workspace(
                    original_entity,
                    entity,
                    data["code"][0]["name"],
                    original_model_code,
                    data["code"][0]["definition"],
                )
                input_ = input("> ")
                if input_.lower() in [":q", ":q!", ":wq"]:
                    self.conversation.newline()

                    if input_.lower() == ":q":
                        self.conversation.type("Exiting without saving.\n")

                    if input_.lower() in [":q", ":q!"]:
                        exit(1)

                    # Mute output from individual merge + rewrite operations
                    self.conversation.mute()

                    with Spinner(
                        "Gibson is saving your changes to the entity...",
                        "Entity saved",
                    ):
                        self.memory.remember_last({"entities": [data["entity"]]})
                        Merge(self.configuration).execute()

                    # Rewrite each category of code with the new entity definition
                    Model(self.configuration).execute(entity_name=entity.name)
                    Schema(self.configuration).execute(entity_name=entity.name)
                    Test(self.configuration).execute(entity_name=entity.name)

                    if original_entity is None:
                        # We need to ensure the testing.py file is updated to import the new entity
                        Base(self.configuration).execute()

                    self.conversation.unmute()
                    self.conversation.type(
                        f"\nAll code for the {Colors.entity(entity.name)} entity has been written 🎉\n\n"
                    )
                    exit()
                elif input_ == "" or input_.startswith(":"):
                    continue

                with ComputingSpinner():
                    talk_to_gibsonai = True
                    parts = input_.split(" ")
                    if parts[0] == "fk":
                        input_ = self.CODE_WRITER_ENTITY_MODIFIER_NOOP
                        if not self.__add_foreign_key(entity, parts[1]):
                            # If the entity was not modified, likely because the table
                            # referenced does not exist or does not contain indexes which
                            # can be used for a foreign key, do not waste the network call
                            # to GibsonAI since there is nothing to do.
                            talk_to_gibsonai = False

                    if talk_to_gibsonai is True:
                        data = cli.code_writer_entity_modifier(
                            self.__context.json,
                            data["entity"]["name"],
                            entity.create_statement(),
                            input_,
                        )
                        entity = (
                            StructureEntity()
                            .instantiate(self.configuration.project.datastore.type)
                            .import_from_struct(data)
                        )
            except KeyboardInterrupt:
                self.conversation.type("\nExiting without saving.\n")
                exit(1)

    def get_default_ref_table_template_path(self):
        return (
            os.path.dirname(__file__)
            + "/../../data/"
            + self.configuration.project.datastore.type
            + "/default-ref-table.tmpl"
        )

    def get_default_table_template_path(self):
        return (
            os.path.dirname(__file__)
            + "/../../data/"
            + self.configuration.project.datastore.type
            + "/default-table.tmpl"
        )

    def __render_workspace(
        self,
        original_entity: StructureEntity | None,
        entity: StructureEntity,
        model_name: str,
        original_model_code: str | None,
        model_code: str,
    ):
        self.configuration.platform.cmd_clear()
        create_table_statement_diff = (
            diff(original_entity.create_statement(), entity.create_statement())
            if original_entity
            else additions(entity.create_statement())
        )
        model_code_diff = (
            diff(original_model_code, model_code)
            if original_model_code
            else additions(model_code)
        )

        print("")
        print(WorkspaceHeader().render(self.configuration.project.name))

        print("")
        print(Header().render("SQL", Colors.cyan))
        print("")
        print(Colors.table(create_table_statement_diff, entity.name))

        print("")
        print(Header().render("Model", Colors.yellow))
        print("")
        print(Colors.model(model_code_diff, model_name, entity.name))
        print(WorkspaceFooter().render())

    def template_definition(self, entity_name):
        parts = entity_name.split("_")
        if len(parts) > 1 and parts[1] == "ref":
            # This is a reference table implementation. We will handle this here.
            with open(self.get_default_ref_table_template_path()) as f:
                definition = Template(f.read()).substitute({"entity_name": entity_name})

                self.memory.append_last({"definition": definition, "name": entity_name})

                self.conversation.type(
                    "Reference table created and stored in last memory. What's next?\n"
                )
                self.conversation.newline()

                exit(1)

        with open(self.get_default_table_template_path()) as f:
            return Template(f.read()).substitute({"entity_name": entity_name})
