from gibson.core.Configuration import Configuration
from gibson.services.code.customization.Authenticator import Authenticator
from gibson.services.code.customization.Index import Index


class CustomizationManager:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.customizations = [
            Authenticator(self.configuration),
            Index(self.configuration),
        ]

    def preserve(self):
        for customization in self.customizations:
            customization.preserve()

        return self

    def restore(self):
        for customization in self.customizations:
            customization.restore()

        return self
