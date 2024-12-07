import json
import os


class PythonPath:
    def __init__(self):
        self.user_home = os.environ.get("HOME")
        self.gibson_config = ".gibsonai"
        self.file_name = "python_path"

    def install(self):
        python_path_location = f"$HOME/{self.gibson_config}/{self.file_name}"
        installation = f"""\n[ -s "{python_path_location}" ] && \\. "{python_path_location}" # Setup pythonpath for gibson projects\n"""

        for file in [f"{self.user_home}/.bashrc", f"{self.user_home}/.zshrc"]:
            with open(file, "a+") as f:
                f.seek(0)
                if python_path_location not in f.read():
                    f.write(installation)

        return self

    def write(self):
        try:
            with open(f"{self.user_home}/{self.gibson_config}/config", "r") as f:
                config = json.loads(f.read())
        except:
            return self

        project_paths = filter(
            lambda x: x is not None,
            [
                config.get(project).get("dev", {}).get("base", {}).get("path")
                for project in config
            ],
        )

        if not project_paths:
            return self

        try:
            os.mkdir(f"{self.user_home}/{self.gibson_config}")
        except FileExistsError:
            pass

        contents = "\n".join(
            f"export PYTHONPATH=$PYTHONPATH:{path}" for path in project_paths
        )
        with open(f"{self.user_home}/{self.gibson_config}/{self.file_name}", "w") as f:
            f.write(contents)

        return self
