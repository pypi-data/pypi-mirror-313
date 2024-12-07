from .Api import Api
from .Code import Code
from .Datastore import Datastore
from .Dev import Dev
from .Modeler import Modeler
from .Paths import ProjectPaths


class Project:
    def __init__(self):
        self.id = None
        self.api = Api()
        self.code = Code()
        self.datastore = Datastore()
        self.description = None
        self.dev = Dev()
        self.modeler = Modeler()
        self.name = None
        self.paths = ProjectPaths()
