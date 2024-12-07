from gibson.api.BaseApi import BaseApi
from gibson.command.BaseCommand import BaseCommand
from gibson.services.auth.Server import Server as AuthServer


class Login(BaseCommand):
    def execute(self):
        authenticated = self.configuration.login()
        if authenticated:
            self.conversation.message_login_success()
        else:
            self.conversation.message_login_failure()
        self.conversation.newline()
