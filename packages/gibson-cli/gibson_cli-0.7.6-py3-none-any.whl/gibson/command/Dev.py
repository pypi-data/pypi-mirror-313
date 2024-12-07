import os
import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.lang.Python import Python


class Dev(BaseCommand):
    def __display_language_specific_instructions(self):
        if self.configuration.project.code.language == "python":
            pythonpath = Python().define_python_path(
                [
                    os.path.expandvars(self.configuration.project.dev.base.path),
                    os.path.expandvars(self.configuration.project.dev.model.path),
                    os.path.expandvars(self.configuration.project.dev.schema.path),
                ]
            )
            if pythonpath is not None:
                self.conversation.type(
                    "Your Python environment needs to be configured, so do this:\n"
                )
                self.conversation.type(
                    f"  export PYTHONPATH=$PYTHONPATH:{pythonpath}\n\n"
                )

        return self

    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] not in ["off", "on"]:
            self.usage()

        self.configuration.require_project()

        if sys.argv[2] == "off":
            if self.configuration.project.dev.active is True:
                self.configuration.turn_dev_off()

            self.off()

        self.configuration.display_project()
        self.conversation.type(
            "Leveling up. Nice! I need a little context to make sure I write "
            + "code\nin the correct place. Then I will need you to tell me "
            + "about how to\nconfigure the API.\n\n"
        )

        api_path = self.configuration.project.dev.api.path
        if api_path is None:
            api_path = ""

        base_path = self.configuration.project.dev.base.path
        if base_path is None:
            base_path = ""

        model_path = self.configuration.project.dev.model.path
        if model_path is None:
            model_path = ""

        schema_path = self.configuration.project.dev.schema.path
        if schema_path is None:
            schema_path = ""

        self.conversation.type(
            "  I need a writable directory into which I can put code.\n"
        )
        base = self.configuration.ask_for_path(base_path)

        for subdir in ["api", "model", "schema"]:
            try:
                os.mkdir(f"{os.path.expandvars(base)}/{subdir}")
            except FileExistsError:
                pass

        self.conversation.type("\n  https://api.yourdomain.com/v1/-/sneakers GET\n")
        self.conversation.type("                             ^  ^\n")
        self.conversation.type("                             |  |\n")
        self.conversation.type("                    version _|  |\n")
        self.conversation.type(
            "                                |_ prefix (to isolate GibsonAI "
            + "API routes)\n\n",
        )
        self.conversation.type(
            "  It is OK if you are not sure about these. Just leave the defaults\n"
            + "  and when you make a decision I will rewrite the code for you.\n\n"
        )

        api_version = self.configuration.ask_for_value(
            "  version", self.configuration.project.dev.api.version
        )
        api_prefix = self.configuration.ask_for_value(
            "   prefix", self.configuration.project.dev.api.prefix
        )

        self.configuration.turn_dev_on(
            f"{base}/api",
            api_prefix,
            api_version,
            base,
            f"{base}/model",
            f"{base}/schema",
        )

        self.conversation.newline()
        self.__display_language_specific_instructions()
        self.conversation.type("Dev Mode is on!\n\n")

        return self

    def off(self):
        self.configuration.display_project()
        self.conversation.type("Dev Mode is off!\n")
        self.conversation.newline()
        exit(1)

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'dev', args=['off', 'on'], hint='turn dev mode on or off')}\n"
        )
        self.conversation.newline()
        exit(1)
