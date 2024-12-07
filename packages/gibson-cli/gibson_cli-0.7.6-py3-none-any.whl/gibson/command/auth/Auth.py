import sys

import gibson.core.Colors as Colors
from gibson.command.auth.Login import Login
from gibson.command.auth.Logout import Logout
from gibson.command.BaseCommand import BaseCommand


class Auth(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()
        elif sys.argv[2] == "login":
            Login(self.configuration).execute()
        elif sys.argv[2] == "logout":
            Logout(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command, 'auth', args=['login', 'logout'])}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'auth', args='login', hint='login to Gibson')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command, 'auth', args='logout', hint='logout of Gibson')}\n"
        )
        self.conversation.newline()
        exit(1)
