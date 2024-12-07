import os

from gibson.core.Configuration import Configuration
from gibson.core.utils import (
    utils_entity_name_to_class_name,
    utils_extract_module_name,
    utils_is_ref_table,
)


class Dev:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def api_component(self, file_name, code):
        self.__write_code(
            self.configuration.project.dev.api.path,
            f"{self.configuration.project.dev.api.version}/{file_name}",
            code,
        )
        return self

    def base_component(self, file_name, code):
        self.__write_code(self.configuration.project.dev.base.path, file_name, code)

    def link(self, base_path, source_file, target_file, overwrite=False):
        target = f"{base_path}/{target_file}"
        if overwrite is False:
            if os.path.isfile(target):
                return self

        os.symlink(f"{base_path}/{source_file}", target)

        return self

    def __mkdirs(self, path):
        os.makedirs(path, exist_ok=True)
        return path

    def model(self, entity_name, code):
        if utils_is_ref_table(entity_name) is True:
            return self

        module = utils_extract_module_name(entity_name)
        file = utils_entity_name_to_class_name(entity_name) + ".py"

        return self.__write_code(
            self.configuration.project.dev.model.path, f"{module}/{file}", code
        )

    def schema(self, entity_name, code):
        if utils_is_ref_table(entity_name) is True:
            return self

        module = utils_extract_module_name(entity_name)
        file = utils_entity_name_to_class_name(entity_name) + ".py"

        return self.__write_code(
            self.configuration.project.dev.schema.path,
            f"{module}/{file}",
            code,
        )

    def tests(self, entity_name, code):
        if utils_is_ref_table(entity_name) is True:
            return self

        module = utils_extract_module_name(entity_name)
        file = "test_" + utils_entity_name_to_class_name(entity_name) + "Base.py"

        return self.__write_code(
            self.configuration.project.dev.model.path, f"{module}/tests/{file}", code
        )

    def __write_code(self, path, file, code):
        if self.configuration.project.dev.active is True:
            full_path = f"{os.path.expandvars(path)}/{file}"

            self.__mkdirs("/".join(full_path.split("/")[0:-1]))
            with open(full_path, "w") as f:
                f.write(code)

        return self
