import os

from .BaseCommand import BaseCommand


class Tree(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        self.configuration.display_project()

        if self.configuration.project.dev.base.path is None:
            self.conversation.configure_dev_mode()
            self.conversation.newline()
            exit(1)

        print(self.configuration.project.dev.base.path)
        base_path = os.path.expandvars(self.configuration.project.dev.base.path)

        if os.path.isfile(f"{base_path}/BaseModel.py"):
            self.render_file("BaseModel.py", 2, False)

        if os.path.isfile(f"{base_path}/BaseSchema.py"):
            self.render_file("BaseSchema.py", 2, False)

        if os.path.isfile(f"{base_path}/Deps.py"):
            self.render_file("Deps.py", 2, False)

        if os.path.isfile(f"{base_path}/Enums.py"):
            self.render_file("Enums.py", 2, False)

        if os.path.isfile(f"{base_path}/Session.py"):
            self.render_file("Session.py", 2, False)

        if os.path.isdir(f"{base_path}/api"):
            self.render_dir("api", 2, False, explanation="FastAPI Application")
            self.list_dir(f"{base_path}/api", 6)

        if os.path.isdir(f"{base_path}/lib"):
            self.render_dir("lib", 2, False, explanation="GibsonAI Libraries")
            self.list_dir(f"{base_path}/lib", 6)

        if os.path.isdir(f"{base_path}/model"):
            self.render_dir("model", 2, False, explanation="SQLAlchemy Models")
            self.list_dir(f"{base_path}/model", 6)

        if os.path.isdir(f"{base_path}/schema"):
            self.render_dir("schema", 2, False, explanation="Pydantic Schemas")
            self.list_dir(f"{base_path}/schema", 6)

        if os.path.isfile(f"{base_path}/testing.py"):
            self.render_file("testing.py", 2, True)

        self.conversation.newline()

    def list_dir(self, path, indent):
        entries = []
        for entry in os.listdir(path):
            if entry not in [".pytest_cache"]:
                if os.path.isdir(path + f"/{entry}"):
                    entry += "/"

                entries.append(entry)

        entries.sort()

        for i in range(len(entries)):
            is_last = i == len(entries) - 1
            if entries[i][-1] == "/":
                self.render_dir(entries[i], indent, is_last)
                self.list_dir(path + "/" + entries[i], indent + 4)
            else:
                self.render_file(entries[i], indent, is_last)

    def render_dir(self, path, indent, is_last, explanation=None):
        char = "-"
        if is_last is True:
            char = "_"

        if path[-1] != "/":
            path += "/"

        explain = ""
        if explanation is not None:
            explain = f"<{explanation}> "

        print(" " * indent + "|" + char * 2 + f" {explain}{path}")

    def render_file(self, name, indent, is_last):
        char = "-"
        if is_last is True:
            char = "_"

        print(" " * indent + "|" + char + f" {name}")
