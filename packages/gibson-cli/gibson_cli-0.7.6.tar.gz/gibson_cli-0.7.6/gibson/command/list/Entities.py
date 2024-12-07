import sys

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

from gibson.command.BaseCommand import BaseCommand


class Entities(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        self.configuration.display_project()

        last = self.memory.recall_last() or []
        stored = self.memory.recall_entities() or []

        if len(last) == 0 and len(stored) == 0:
            self.conversation.nothing_to_list(sys.argv[2])
            self.conversation.newline()
        else:
            console = Console()
            table = Table(
                title="Entities",
                header_style="bold",
                box=box.ROUNDED,
                leading=1,
            )
            table.add_column("Name", style="magenta", header_style="magenta")
            table.add_column("Memory")

            for entity in sorted(stored, key=lambda x: x["name"]):
                table.add_row(entity["name"], Text("stored", style="green"))

            for entity in sorted(last, key=lambda x: x["name"]):
                table.add_row(entity["name"], Text("last", style="yellow"))

            console.print(table)
