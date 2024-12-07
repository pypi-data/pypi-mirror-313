from gibson.api.BaseApi import BaseApi
from gibson.core.Configuration import Configuration
from gibson.core.Memory import Memory
from gibson.lang.Python import Python


class Cli(BaseApi):
    PREFIX = "cli"

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.configuration.require_login()
        self.configuration.require_project()
        self.configuration.require_project_key_or_id()

    def code_api(self):
        return self.post(
            "code/api",
            self.__structure_context_payload(self.configuration, with_stored=True),
        ).json()

    def code_base(self):
        return self.post(
            "code/base",
            self.__structure_context_payload(self.configuration, with_stored=True),
        ).json()

    def code_model_attributes(self, model_name, instructions):
        payload = self.__structure_context_payload(self.configuration)
        payload["model"] = {"name": model_name}
        payload["q"] = instructions

        return self.post("code/model/attributes", payload).json()

    def code_models(self, entities: list):
        payload = self.__structure_context_payload(self.configuration, with_stored=True)
        payload["entities"] = entities

        return self.post("code/models", payload).json()

    def code_schemas(self, entities: list):
        payload = self.__structure_context_payload(self.configuration, with_stored=True)
        payload["entities"] = entities

        return self.post("code/schemas", payload).json()

    def code_testing(self, entities: list):
        payload = self.__structure_context_payload(self.configuration, with_stored=True)
        payload["entities"] = entities

        return self.post("code/testing", payload).json()

    def code_writer_entity_modifier(self, context, name, definition, instructions):
        payload = self.__structure_context_payload(self.configuration)
        payload["context"] = context
        payload["entity"] = {"definition": definition, "name": name}
        payload["q"] = instructions

        return self.post("code/writer/entity/modifier", payload).json()

    def code_writer_schema_context(self):
        return self.post(
            "code/writer/schema/context",
            self.__structure_context_payload(self.configuration, with_stored=True),
        ).json()

    def headers(self):
        headers = super().headers()
        if self.configuration.project.id:
            headers["X-Gibson-Project-ID"] = self.configuration.project.id
        else:
            headers["X-Gibson-API-Key"] = self.configuration.project.api.key
        return headers

    def import_(self):
        return self.get("import")

    def llm_query(self, instructions, has_file, has_python, has_sql):
        project_config = self.configuration.project

        r = self.post(
            "llm/query",
            {
                "content": {
                    "meta": {
                        "file": int(has_file),
                        "python": int(has_python),
                        "sql": int(has_sql),
                    }
                },
                "datastore": {"type": project_config.datastore.type},
                "frameworks": {
                    "api": project_config.code.frameworks.api,
                    "model": project_config.code.frameworks.model,
                    "revision": project_config.code.frameworks.revision,
                    "schema_": project_config.code.frameworks.schema,
                    "test": project_config.code.frameworks.test,
                },
                "q": instructions,
            },
        )

        return r.json()

    def modeler_entity_modify(
        self, modeler_version, project_description, entity: dict, modifications: str
    ):
        r = self.put(
            "modeler/entity/modify",
            {
                "datastore": {"type": self.configuration.project.datastore.type},
                "entity": entity,
                "modeler": {"version": modeler_version},
                "modifications": modifications,
                "project": {"description": project_description},
            },
        )

        return r.json()

    def modeler_entity_remove(self, modeler_version, entities: list, entity_name):
        r = self.put(
            "modeler/entity/remove",
            {
                "datastore": {"type": self.configuration.project.datastore.type},
                "entity": {"name": entity_name},
                "modeler": {"version": modeler_version},
                "schema_": entities,
            },
        )

        return r.json()

    def modeler_entity_rename(self, modeler_version, entities: list, current, new):
        r = self.put(
            "modeler/entity/rename",
            {
                "datastore": {"type": self.configuration.project.datastore.type},
                "entity": {"current": current, "new": new},
                "modeler": {"version": modeler_version},
                "schema_": entities,
            },
        )

        return r.json()

    def modeler_module(self, modeler_version, project_description, module):
        r = self.post(
            "modeler/module",
            {
                "datastore": {"type": self.configuration.project.datastore.type},
                "modeler": {"version": modeler_version},
                "module": module,
                "project": {"description": project_description},
            },
        )

        return r.json()

    def modeler_openapi(self, modeler_version, contents):
        r = self.post(
            "modeler/openapi",
            {
                "contents": contents,
                "datastore": {"type": self.configuration.project.datastore.type},
                "modeler": {"version": modeler_version},
            },
        )

        return r.json()

    def modeler_reconcile(self, modeler_version, entities: list):
        r = self.post(
            "modeler/reconcile",
            {
                "datastore": {"type": self.configuration.project.datastore.type},
                "modeler": {"version": modeler_version},
                "schema_": entities,
            },
        )

        return r.json()

    def __structure_context_payload(
        self,
        with_last=False,
        with_merged=False,
        with_stored=False,
    ):
        project_config = self.configuration.project

        payload = {
            "api": {
                "prefix": project_config.dev.api.prefix,
                "version": project_config.dev.api.version,
            },
            "datastore": {"type": project_config.datastore.type},
            "frameworks": {
                "api": project_config.code.frameworks.api,
                "model": project_config.code.frameworks.model,
                "revision": project_config.code.frameworks.revision,
                "schema_": project_config.code.frameworks.schema,
                "test": project_config.code.frameworks.test,
            },
            "language": project_config.code.language,
            "path": {
                "api": Python().make_import_path(project_config.dev.api.path),
                "base": Python().make_import_path(project_config.dev.base.path),
                "custom": {
                    "model": {
                        "class_": project_config.code.custom.model_class,
                        "path": project_config.code.custom.model_path,
                    }
                },
                "model": Python().make_import_path(project_config.dev.model.path),
                "schema_": Python().make_import_path(project_config.dev.schema.path),
            },
        }

        if with_last is True:
            payload["schema_"] = Memory(self.configuration).recall_last()["entities"]
        elif with_merged is True:
            payload["schema_"] = Memory(self.configuration).recall_merged()
        elif with_stored is True:
            payload["schema_"] = Memory(self.configuration).recall_entities()

        return payload
