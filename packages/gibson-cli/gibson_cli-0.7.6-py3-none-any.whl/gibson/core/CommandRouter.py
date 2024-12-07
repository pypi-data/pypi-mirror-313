import sys

from gibson.command.auth.Auth import Auth
from gibson.command.Build import Build
from gibson.command.code.Code import Code
from gibson.command.Conf import Conf
from gibson.command.Count import Count
from gibson.command.Dev import Dev
from gibson.command.Forget import Forget
from gibson.command.Help import Help
from gibson.command.importer.Import import Import
from gibson.command.list.List import List
from gibson.command.Merge import Merge
from gibson.command.Modify import Modify
from gibson.command.new.New import New
from gibson.command.Question import Question
from gibson.command.Remove import Remove
from gibson.command.rename.Rename import Rename
from gibson.command.rewrite.Rewrite import Rewrite
from gibson.command.Show import Show
from gibson.command.Tree import Tree
from gibson.command.Version import Version
from gibson.core.Configuration import Configuration
from gibson.core.Conversation import Conversation
from gibson.core.Env import Env


class CommandRouter:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.conversation = Conversation()

    def run(self):
        if len(sys.argv) == 1:
            Help(self.configuration).execute()
            return self

        Env().verify(self.configuration)

        command = None
        if sys.argv[1] == "auth":
            command = Auth(self.configuration)
        elif sys.argv[1] == "build":
            command = Build(self.configuration)
        elif sys.argv[1] == "code":
            command = Code(self.configuration)
        elif sys.argv[1] == "conf":
            command = Conf(self.configuration)
        elif sys.argv[1] == "count":
            command = Count(self.configuration)
        elif sys.argv[1] == "dev":
            command = Dev(self.configuration)
        elif sys.argv[1] == "forget":
            command = Forget(self.configuration)
        elif sys.argv[1] == "help":
            command = Help(self.configuration)
        elif sys.argv[1] == "import":
            command = Import(self.configuration)
        elif sys.argv[1] == "list":
            command = List(self.configuration)
        elif sys.argv[1] == "merge":
            command = Merge(self.configuration)
        elif sys.argv[1] == "modify":
            command = Modify(self.configuration)
        elif sys.argv[1] == "new":
            command = New(self.configuration)
        elif sys.argv[1] == "remove":
            command = Remove(self.configuration)
        elif sys.argv[1] == "rename":
            command = Rename(self.configuration)
        elif sys.argv[1] == "rewrite":
            command = Rewrite(self.configuration, with_header=True)
        elif sys.argv[1] == "show":
            command = Show(self.configuration)
        elif sys.argv[1] == "tree":
            command = Tree(self.configuration)
        elif sys.argv[1] in ["q"]:
            command = Question(self.configuration)
        elif sys.argv[1] in ["version", "--version", "-v"]:
            command = Version(self.configuration)

        if command is None or command.execute() is False:
            Help(self.configuration).execute()
            exit(1)
