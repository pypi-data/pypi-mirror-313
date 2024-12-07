import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand


class Conf(BaseCommand):
    def __compile_configuration_keys(self, element, setting, keys):
        if not isinstance(element, dict):
            keys.append("::".join(setting))
        else:
            for key, value in element.items():
                if key not in ["dev", "modeler"]:
                    self.__compile_configuration_keys(
                        element[key], setting + [key], keys
                    )

        return keys

    def execute(self):
        if len(sys.argv) != 4 or sys.argv[2] not in self.get_configuration_keys():
            self.usage()

        settings = self.configuration.get_my_settings()
        key = sys.argv[2]
        value = sys.argv[3]
        item = settings

        elements = key.split("::")
        for i in range(len(elements) - 1):
            try:
                item = item[elements[i]]
            except KeyError:
                self.usage()

        try:
            old_value = item[elements[-1]]
            item[elements[-1]] = value
        except KeyError:
            self.usage()

        self.configuration.require_project()
        self.configuration.display_project()
        self.conversation.type(f"{key}\n")
        self.conversation.type(f"  [old value] {old_value}\n")
        self.conversation.type(f"  [new value] {value}\n")
        self.conversation.newline()
        self.configuration.write_config()

        return self

    def get_configuration_keys(self):
        configuration_keys = self.__compile_configuration_keys(
            self.configuration.get_my_settings(), [], []
        )

        del configuration_keys[configuration_keys.index("meta::version")]

        return configuration_keys

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'conf', args='[key]', inputs='[value]', hint='set a configuration value')}\n"
        )
        self.conversation.newline()

        if self.configuration.project:
            self.conversation.type(f"  where {Colors.argument('[key]')} is one of:\n")

            for key in self.get_configuration_keys():
                self.conversation.type(f"    {key}\n")

            self.conversation.newline()

        exit(1)
