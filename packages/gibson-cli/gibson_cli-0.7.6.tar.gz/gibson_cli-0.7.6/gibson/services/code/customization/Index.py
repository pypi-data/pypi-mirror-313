import os

from gibson.services.code.customization.BaseCustomization import BaseCustomization


class Index(BaseCustomization):
    def _get_file_name(self):
        return os.path.expandvars(
            self.configuration.project.dev.api.path
            + "/"
            + self.configuration.project.dev.api.version
            + "/routers/index.py"
        )
