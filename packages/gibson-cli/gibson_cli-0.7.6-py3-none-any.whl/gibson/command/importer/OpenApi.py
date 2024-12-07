import json
import re
import sys

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand


class OpenApi(BaseCommand):
    def bad_json(self):
        self.configuration.display_project()
        self.conversation.type(
            "I need valid JSON. That file does not appear to be that. Try again?\n"
        )
        self.conversation.newline()
        exit(1)

    def execute(self):
        try:
            with open(sys.argv[3], "r") as f:
                contents = json.loads(f.read())
        except FileNotFoundError:
            self.configuration.display_project()
            self.conversation.file_not_found(sys.argv[3])
            self.conversation.newline()
            exit(1)
        except json.decoder.JSONDecodeError:
            self.bad_json()

        if "paths" not in contents:
            self.unrecognized_format()

        self.configuration.require_project()
        self.configuration.display_project()

        if contents.get("info", None) is not None:
            if contents["info"].get("title", None) is not None:
                self.conversation.type(contents["info"]["title"])
                self.conversation.newline()

        path_list = []
        for path, description in contents["paths"].items():
            path_list.append(path)

        path_list.sort()

        i = 0
        for path in path_list:
            self.conversation.type(f"   {i}: ".rjust(10) + path + "\n")
            i += 1

        self.conversation.newline()

        self.conversation.type(
            "Now tell me which ones you want me to build for you. You can provide a "
            + 'single\nnumber, a comma separated list of numbers or "all" to build '
            + "everything.\n"
        )
        self.conversation.newline()

        selection = ""
        while len(selection) == 0:
            selection = input("What should I build? ")

        selection_list = re.sub(" ", "", selection.lower()).split(",")

        choices = []
        if "all" in selection_list:
            choices = path_list
        else:
            for choice in selection_list:
                try:
                    choices.append(path_list[int(choice)])
                except (IndexError, ValueError):
                    pass

        self.conversation.newline()

        if len(choices) == 0:
            exit(1)

        cli = Cli(self.configuration)
        self.conversation.type("Building schema...\n")

        entities = []
        for choice in choices:
            self.conversation.type("    " + choice + "\n")

            response = cli.modeler_openapi(
                self.configuration.project.modeler.version,
                json.dumps(contents["paths"][choice]),
            )

            for entity in response["entities"]:
                entities.append(entity)
                self.conversation.type(" " * 8 + entity["name"])
                self.conversation.newline()

        self.conversation.type("Reconciling schema...\n")
        response = cli.modeler_reconcile(
            self.configuration.project.modeler.version, entities
        )

        self.memory.remember_last(response)

        word_entities = "entities"
        if len(response["entities"]) == 1:
            word_entities = "entity"

        self.conversation.type("\nSummary\n")
        self.conversation.type(
            f"    {len(response['entities'])} {word_entities} imported\n"
        )
        self.conversation.newline()

        return True

    def unrecognized_format(self):
        self.configuration.display_project()
        self.conversation.type(
            "Well that sucks. I do not recognize this JSON format.\n"
        )
        self.conversation.newline()
        exit(1)
