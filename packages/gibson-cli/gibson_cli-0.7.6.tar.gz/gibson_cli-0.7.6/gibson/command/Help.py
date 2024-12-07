from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Memory import Memory


class Help(BaseCommand):
    def execute(self):
        dev_mode_text = []

        if self.configuration.project is not None:
            dev_mode = "on" if self.configuration.project.dev.active is True else "off"
            dev_color = (
                "green" if self.configuration.project.dev.active is True else "red"
            )
            dev_mode_text = [
                "\n\ndev mode is turned ",
                (dev_mode, f"bold {dev_color}"),
            ]

        subcommands = {
            "auth": {
                "description": "authenticate with the gibson cli",
                "subcommands": ["login", "logout"],
                "memory": None,
            },
            "build": {
                "description": "create the entities in the datastore",
                "subcommands": ["datastore"],
                "memory": "stored",
            },
            "code": {
                "description": "pair program with gibson",
                "subcommands": ["api", "base", "entity", "models", "schemas", "tests"],
                "memory": None,
            },
            "conf": {
                "description": "set a configuration variable",
                "subcommands": None,
                "memory": None,
            },
            "count": {
                "description": "show the number of entities stored",
                "subcommands": ["last", "stored"],
                "memory": "based on user selection",
            },
            "dev": {
                "description": Text.assemble(
                    "gibson will automatically write code for you",
                    *dev_mode_text,
                ),
                "subcommands": ["on", "off"],
                "memory": None,
            },
            "forget": {
                "description": f"delete entities from memory",
                "subcommands": ["all", "last", "stored"],
                "memory": "based on user selection",
            },
            "help": {"description": "for help", "subcommands": None, "memory": None},
            "import": {
                "description": "import entities from a datasource",
                "subcommands": ["api", "mysql", "pg_dump", "openapi"],
                "memory": "stored",
            },
            "list": {
                "description": "see a list of your entities or projects",
                "subcommands": ["entities", "projects"],
                "memory": None,
            },
            "merge": {
                "description": "merge last memory (recent changes) into stored project memory",
                "subcommands": None,
                "memory": "last -> stored",
            },
            "modify": {
                "description": "change an entity using natural language",
                "subcommands": None,
                "memory": "last > stored",
            },
            "new": {
                "description": "create something new",
                "subcommands": ["project", "module", "entity"],
                "memory": None,
            },
            "remove": {
                "description": "remove an entity from the project",
                "subcommands": None,
                "memory": "last > stored",
            },
            "rename": {
                "description": "rename an entity",
                "subcommands": ["entity"],
                "memory": "last > stored",
            },
            "rewrite": {
                "description": "rewrite all code",
                "subcommands": None,
                "memory": "stored",
            },
            "show": {
                "description": "display an entity",
                "subcommands": None,
                "memory": "last > stored",
            },
            "tree": {
                "description": "illustrate the project layout in a tree view",
                "subcommands": None,
                "memory": None,
            },
            "q": {
                "description": "ask gibson a question using natural language",
                "subcommands": None,
                "memory": None,
            },
        }

        self.configuration.display_project()

        console = Console()

        help = Table(
            title=Text.assemble(
                "usage: ",
                (self.configuration.command, "green bold"),
                (" [command]", "yellow bold"),
                (" [subcommand]", "magenta bold"),
            ),
            header_style="bold",
            box=box.ROUNDED,
            expand=True,
            leading=1,
        )
        help.add_column("command", style="yellow bold", header_style="yellow bold")
        help.add_column("description")
        help.add_column("subcommands", header_style="magenta")
        help.add_column("memory affected", style="grey50", header_style="grey50")

        for subcommand, config in subcommands.items():
            help.add_row(
                subcommand,
                config["description"],
                (
                    Text(" | ").join(
                        Text(x, style="magenta") for x in config["subcommands"]
                    )
                    if config["subcommands"]
                    else ""
                ),
                config["memory"] or "",
            )

        console.print(help)

        self.conversation.newline()

        if self.configuration.project:
            stats = Memory(self.configuration).stats()
            memory = Table(
                title="Memory",
                show_header=True,
                header_style="bold",
                box=box.ROUNDED,
                expand=True,
            )
            memory.add_column("stored", style="green", header_style="green")
            memory.add_column("last", style="yellow", header_style="yellow")
            memory.add_row(
                f"{stats['entities']['num']} {stats['entities']['word']}",
                f"{stats['last']['num']} {stats['last']['word']}",
            )
            console.print(memory)
