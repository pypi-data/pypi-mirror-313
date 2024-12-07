from rich import box
from rich.console import Console
from rich.table import Table

import gibson.core.Colors as Colors
from gibson.api.ProjectApi import ProjectApi
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Spinner import DisappearingSpinner


class Projects(BaseCommand):
    def execute(self):
        self.configuration.require_login()

        with DisappearingSpinner():
            projects = ProjectApi(self.configuration).all_projects()

        if len(projects) == 0:
            self.conversation.type(
                f"No projects found. Create one with {Colors.command(self.configuration.command, 'new', args='project')}\n"
            )
            exit(1)

        console = Console()
        table = Table(
            title="Projects",
            header_style="bold magenta",
            box=box.ROUNDED,
            leading=1,
        )
        table.add_column("Name")
        table.add_column("ID", min_width=36)

        for project in projects:
            name = project["name"] if project["name"] is not None else "Untitled"
            table.add_row(
                name,
                project["uuid"],
            )

        console.print(table)
