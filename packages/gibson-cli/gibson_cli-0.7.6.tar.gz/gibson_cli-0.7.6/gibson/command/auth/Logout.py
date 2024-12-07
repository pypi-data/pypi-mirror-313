from gibson.command.BaseCommand import BaseCommand


class Logout(BaseCommand):
    def execute(self):
        self.configuration.set_access_token(None)
        self.conversation.type(f"You are now logged out.")
        self.conversation.newline()
