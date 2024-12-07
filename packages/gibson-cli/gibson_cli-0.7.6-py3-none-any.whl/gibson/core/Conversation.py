import re
import sys
import threading
import time

import pyfiglet

import gibson.core.Colors as Colors
from gibson.conf.Version import Version


class Conversation:
    DEFAULT_DELAY = 0

    def __init__(self):
        self.__mute = False

    def c64_boot_loading(self):
        self.type("LOADING\n")
        return self

    def c64_ready_run(self):
        self.type("READY.\n")
        self.type("RUN")
        return self

    def c64_boot_search(self):
        self.type("    **** COMMODORE 64 BASIC V2 ****\n")
        self.type(" 64K RAM SYSTEM  38911 BASIC BYTES FREE\n\n")
        self.type("READY.\n")
        self.type('LOAD "*",8,1\n\n')
        self.type("SEARCHING FOR *\n")
        return self

    def cant_no_entities(self, project_name):
        self.display_project(project_name)
        self.type("I would love to but you have not defined any entities.\n\n")
        return self

    def clear_line(self):
        if self.__mute is True:
            return self

        print("\033[1A\033[K", end="")

    def configure_dev_mode(self):
        self.type(
            "I would love to do that for you but you have not configured "
            + "dev mode yet.\nExecute:\n\n    gibson dev on"
        )
        self.newline()

    def configure_new_project(self, configuration):
        self.type(
            "\nI am so excited that we're building something new together. "
            + "You probably need\nto execute:\n\n"
            + "  gibson conf api::key         [API key]\n"
            + "  gibson conf datastore::type  [datastore type]\n"
            + "  gibson conf datastore::uri   [datastore URI]\n\n"
            + "To finish setting things up.\n"
        )
        self.newline()

        if len(configuration.settings.keys()) > 1:
            self.type(
                "Now that you have more than one project configured, execute one "
                + "of the following:\n\n"
            )

            for key in configuration.settings.keys():
                self.type(f"  export GIBSONAI_PROJECT={key}\n")

            self.newline()

    def display_project(self, project_name):
        self.type(f"<> Project {Colors.project(project_name)}\n\n")

    def entities_hijacked(self):
        self.type(
            "GibsonAI here, I hijacked a bunch of entities. They are in last memory."
        )
        return self

    def file_not_found(self, file_path):
        self.type(f'404, My Friend. Cannot find file "{file_path}".\n')

    def gibsonai_project_not_set(self, configuration):
        self.type(
            "\nYou have to set the environment variable GIBSONAI_PROJECT "
            + "because you have\nmore than one project. Execute one of "
            + "the following statements:\n"
        )
        self.newline()

        for key in configuration.settings.keys():
            self.type(f"  export GIBSONAI_PROJECT={key}\n")

        self.newline()

    def message_configuration_added(self, config_path, section):
        self.type(f"I store my configuration in this file:\n\n{config_path}\n\n")
        self.type("And I just added this section to the configuration:\n\n")
        self.type(f"{section}\n")
        return self

    def message_customize_settings(self):
        self.type(
            f"You can edit the configuration file directly or ask me to do it for you.\n"
        )
        self.type(
            "I will not be able to do much until you modify api::key and "
            + "datastore::uri.\n"
        )
        return self

    def message_environment(self):
        self.type(
            "If you set the environment variable GIBSONAI_PROJECT you can get straight\n"
        )
        self.type(
            "to it. Or, if your configuration file only has one project, I will default\n"
        )
        self.type("to that.\n")
        return self

    def message_explain_help(self):
        self.type('Last item of business, if you need help just type "gibson help".\n')
        return self

    def message_login_failure(self):
        self.newline()
        self.type("Login failed, please try again.\n")
        return self

    def message_login_required(self, configuration):
        self.type("You need to login before performing this action.\n")
        self.type(
            f"Run {Colors.command(configuration.command, 'auth', args='login')} and try again.\n"
        )
        return self

    def message_login_success(self):
        self.newline()
        self.type("Nice! You're now logged in.\n")
        return self

    def message_new_project(self, project_name):
        self.type(
            f"\n{project_name} is going to be huge! Congratulations on the new project.\n\n"
        )
        return self

    def message_welcome(self):
        self.newline()
        print(pyfiglet.figlet_format("GibsonAI", font="big").rstrip(), end="")
        print(f"  ...CLI v{Version.num}...")
        self.newline()
        self.type("Welcome to Gibson!\n")
        self.pause()
        self.newline()
        self.type("First, let's get you logged in.\n")
        self.pause()
        return self

    def message_project_setup(self):
        self.newline()
        self.type(
            "Now let's set up your first project. Give me the name of the project you're working on.\n"
        )
        self.type(
            "Don't worry, once we get to know each other you'll be able to modify this\n"
        )
        self.type("or add new projects on your own.\n")
        return self

    def mute(self):
        self.__mute = True
        return self

    def muted(self):
        return self.__mute is True

    def newline(self):
        if self.__mute is True:
            return self

        print("")

    def new_project(self, configuration):
        self.newline()
        print(pyfiglet.figlet_format("GibsonAI", font="big").rstrip(), end="")
        print(f"  ...CLI v{Version.num}...")
        self.newline()

        if len(configuration.settings.keys()) <= 1:
            self.type("Phew. You like me. Let's do this.\n\n")
        else:
            self.type("Back...again? You know what to do.\n\n")

    def not_sure_no_entity(self, configuration, entity_name):
        self.display_project(configuration.project.name)
        self.type(
            f"No entity named {Colors.entity(entity_name)} exists. You can create it by executing:\n\n"
        )
        self.type(
            f"{Colors.command(configuration.command, 'code', args='entity', inputs=entity_name)}\n\n"
        )
        return self

    def nothing_to_list(self, whats_being_listed):
        self.type(f"No {whats_being_listed} to list.")
        self.newline()

    def pause(self):
        time.sleep(1)

    def project_already_exists(self, project_name):
        self.type(f'\nA project named "{project_name}" already exists.\n')
        self.newline()

    def project_api_key_not_set(self, configuration):
        self.type(
            f"\nYou have not set the API key for your project. Please set the API key by executing:\n"
        )
        self.newline()
        self.type(
            f"{Colors.command(configuration.command, 'conf', args='api::key', inputs='[API key]')}\n"
        )
        self.newline()
        self.type(
            f"If you don't have an API key, you can get one by creating a new project at {Colors.link(configuration.app_domain() + '/chat')}\n"
        )
        self.newline()

    def prompt_module(self):
        while True:
            self.type("Module Name [a-z0-9] > ")
            user_prompt = input("")
            if re.search("^[a-z0-9]+$", user_prompt):
                return user_prompt

    def prompt_project(self):
        while True:
            self.type("Project Name [A-Za-z0-9_-] > ")
            user_prompt = input("")
            if re.search("^[A-Za-z0-9_-]+$", user_prompt):
                return user_prompt

    def prompt_project_description(self, project_name):
        while True:
            self.type(f"Tell me about {project_name}. Don't be shy > ")
            user_prompt = input("")
            if len(user_prompt) > 0:
                return user_prompt

    def prompt_project_id(self):
        while True:
            self.type("Project ID (UUID) > ")
            user_prompt = input("")

            if user_prompt == "":
                return None

            if re.search(
                "^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$",
                user_prompt,
                re.IGNORECASE,
            ):
                return user_prompt

    def raw_llm_response(self):
        print("\n+" + "-" * 75 + "+")
        print("| Raw LLM Response" + " " * 58 + "|")
        print("+" + "-" * 75 + "+\n")
        return self

    def spin(self, thread: threading.Thread):
        animation = self.spinner()
        while thread.is_alive():
            sys.stdout.write(next(animation))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")

    def spinner(self):
        while True:
            for cursor in "|/-\\":
                yield cursor

    def type(self, message, delay=DEFAULT_DELAY):
        if self.__mute is True:
            return self

        try:
            for char in message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        except KeyboardInterrupt:
            exit(1)

    def unmute(self):
        self.__mute = False
        return self

    def unrecognized_project(self, configuration, project_name):
        self.type(
            f'\nYou have not configured a project called "{project_name}". There '
            + "are two paths forward:\n"
        )
        self.newline()

        self.type("  gibson new project\n")
        self.newline()

        self.type(f'To create a project called "{project_name}", or:\n')
        self.newline()

        for key in configuration.settings.keys():
            self.type(f"  export GIBSONAI_PROJECT={key}\n")

        self.newline()
        self.type("To correctly set the environment variable.\n")
        self.newline()

    def wait(self):
        self.newline()
        self.type("<Press Enter>")
        input("")
        self.clear_line()
