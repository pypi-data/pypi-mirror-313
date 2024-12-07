from gibson.core.Configuration import Configuration
from gibson.core.Memory import Memory


class BaseCommand:
    def __init__(self, configuration: Configuration):
        self.__enable_customization_management = True
        self.configuration = configuration
        self.conversation = self.configuration.conversation
        self.memory = Memory(self.configuration)

    def customization_management_is_enabled(self):
        return self.__enable_customization_management == True

    def disable_customization_management(self):
        self.__enable_customization_management = False
        return self

    def execute(self):
        raise NotImplementedError

    def num_required_args(self):
        raise NotImplementedError

    def usage(self):
        return self
