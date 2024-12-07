from gibson.api.BaseApi import BaseApi
from gibson.core.Configuration import Configuration


class ProjectApi(BaseApi):
    PREFIX = "project"

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.configuration.require_login()

    def all_projects(self):
        return self.get("all")["projects"]
