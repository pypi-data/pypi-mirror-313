import os

from gibson.core.Configuration import Configuration


class BaseCustomization:
    def __init__(self, configuration: Configuration):
        self.__link_target = None
        self.__file_contents = None
        self.configuration = configuration

    def _get_file_name(self):
        raise NotImplementedError

    def preserve(self):
        file_name = self._get_file_name()

        if os.path.islink(file_name):
            self.__link_target = os.readlink(file_name)
        elif os.path.isfile(file_name):
            with open(file_name, "r") as f:
                self.__file_contents = f.read()

        return self

    def restore(self):
        file_name = self._get_file_name()

        if self.__link_target is not None:
            try:
                os.unlink(file_name)
            except FileNotFoundError:
                pass

            os.symlink(self.__link_target, file_name)
        elif self.__file_contents is not None:
            try:
                os.unlink(file_name)
            except FileNotFoundError:
                pass

            with open(file_name, "w") as f:
                f.write(self.__file_contents)

        return self
