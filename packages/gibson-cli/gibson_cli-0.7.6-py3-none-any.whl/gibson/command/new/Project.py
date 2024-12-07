from gibson.command.BaseCommand import BaseCommand


class Project(BaseCommand):
    def execute(self):
        self.conversation.new_project(self.configuration)
        project_name = self.conversation.prompt_project()
        if project_name in self.configuration.settings:
            self.conversation.project_already_exists(project_name)
            exit(1)

        project_description = self.conversation.prompt_project_description(project_name)

        self.configuration.set_project_env(project_name)
        self.configuration.append_project_to_conf(project_name, project_description)
        self.configuration.setup_project()
        self.configuration.create_project_memory()

        self.conversation.configure_new_project(self.configuration)
