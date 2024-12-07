import os


class Completions:
    def __init__(self):
        self.user_home = os.environ.get("HOME")
        self.gibson_config = ".gibsonai"
        self.file_name = "bash_completion"

    def install(self):
        completions_location = f"$HOME/{self.gibson_config}/{self.file_name}"
        installation = f"""\n[ -s "{completions_location}" ] && \\. "{completions_location}" # Load gibson auto completion\n"""

        for file in [f"{self.user_home}/.bashrc", f"{self.user_home}/.zshrc"]:
            with open(file, "a+") as f:
                f.seek(0)
                if completions_location not in f.read():
                    f.write(installation)

        return self

    def write(self):
        try:
            file = os.path.dirname(__file__) + f"/../data/bash-completion.tmpl"
            with open(file, "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return self

        try:
            os.mkdir(f"{self.user_home}/{self.gibson_config}")
        except FileExistsError:
            pass

        with open(f"{self.user_home}/{self.gibson_config}/{self.file_name}", "w") as f:
            f.write(contents)

        return self
