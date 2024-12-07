import os


class Python:
    def define_python_path(self, paths: list):
        additions = []
        for entry in paths:
            path = self.make_python_path(entry)
            if path is not None:
                add_path = True
                for addition in additions:
                    if addition in path:
                        add_path = False
                        break

                if add_path:
                    additions.append(path)

        if additions == []:
            return None

        return ":".join(additions)

    def make_import_path(self, os_path):
        if os_path is None:
            return None

        os_path = os.path.expandvars(os_path)

        pythonpath = os.environ.get("PYTHONPATH", "").split(":")
        for entry in pythonpath:
            path = os_path.replace(entry, "")
            if path != os_path:
                path = path.replace("/", ".")
                if path in [None, ""]:
                    # There is no import path, the file is at the top level.  Note,
                    # this is explicitly not None as that will cause the back end
                    # to incorrectly exclude the import.
                    return ""

                if path[0] == ".":
                    path = path[1:]

                return path

        print(
            "Cannot make import path. Please execute the following command in your terminal:\n\n"
        )
        print(f"    export PYTHONPATH=$PYTHONPATH:{os_path}\n\n")
        print("and then try again.\n")
        exit(1)

    def make_python_path(self, path):
        pythonpath = os.environ["PYTHONPATH"].split(":")
        for entry in pythonpath:
            if entry in path:
                return None

        return path
