import errno
import json
import os
import sys

from gibson.conf.Dependencies import Dependencies
from gibson.conf.Paths import ConfigPaths
from gibson.conf.Platform import Platform
from gibson.conf.Project import Project
from gibson.core.Completions import Completions
from gibson.core.Conversation import Conversation
from gibson.core.PythonPath import PythonPath
from gibson.services.auth.Server import Server as AuthServer


class Configuration:
    VERSION = 2
    API_ENV = os.environ.get("GIBSONAI_API_ENV", "production")

    def __init__(self):
        self.command = None
        if len(sys.argv) >= 1:
            self.command = sys.argv[0].split("/")[-1]

        self.conversation = Conversation()
        self.platform = Platform()
        self.project = None
        self.paths = ConfigPaths()
        self.settings = None

        self.set_config_paths()
        self.read_config()
        self.__check_for_configuration_migration()
        self.setup_project()

        Completions().write().install()
        PythonPath().write().install()

    def api_domain(self):
        domains = {
            "local": "http://localhost:8000",
            "staging": "https://staging-api.gibsonai.com",
            "production": "https://api.gibsonai.com",
        }
        return domains[self.API_ENV]

    def app_domain(self):
        domains = {
            "local": "http://localhost:5173",
            "staging": "https://staging-app.gibsonai.com",
            "production": "https://app.gibsonai.com",
        }
        return domains[self.API_ENV]

    def client_id(self):
        return {
            "local": "9b0cbebd-3eb4-47be-89ac-4aa589316ff4",
            "staging": "02459e16-f356-4c01-b689-59847ed04b0a",
            "production": "da287371-240b-4b53-bfde-4b1581cca62a",
        }[self.API_ENV]

    def append_project_to_conf(
        self, project_name, project_description, project_id=None
    ):
        self.project = Project()
        self.project.id = project_id
        self.project.api.key = "FIXME"
        self.project.name = project_name
        self.project.datastore.type = "mysql"
        self.project.datastore.uri = "mysql+pymysql://user:password@host/database_name"
        self.project.description = project_description

        dependencies = Dependencies().compute()

        if self.settings is None:
            self.settings = {}

        self.settings[self.project.name] = {
            "id": self.project.id,
            "api": {"key": self.project.api.key},
            "code": {
                "custom": {"model": {"class": None, "path": None}},
                "frameworks": {
                    "api": dependencies.api,
                    "model": dependencies.model,
                    "revision": dependencies.revision,
                    "schema": dependencies.schema,
                    "test": dependencies.test,
                },
                "language": "python",
            },
            "datastore": {
                "type": self.project.datastore.type,
                "uri": self.project.datastore.uri,
            },
            "dev": {
                "active": False,
                "api": {"path": None, "prefix": "-", "version": "v1"},
                "base": {"path": None},
                "model": {
                    "path": None,
                },
                "schema": {"path": None},
            },
            "meta": {
                "project": {"description": self.project.description},
                "version": self.VERSION,
            },
            "modeler": {"version": "generic-v7"},
        }

        self.write_config()

        # Return a printable version of the project configuration
        return json.dumps(
            {self.project.name: self.settings[self.project.name]}, indent=2
        )

    def ask_for_path(self, current_value):
        while True:
            path = input(f"  [{current_value}]: > ")
            if path in [None, ""]:
                if current_value not in [None, ""]:
                    path = current_value

            test_file = f"{os.path.expandvars(path)}/gibsonai-test-file"

            try:
                with open(test_file, "w") as f:
                    pass

                os.remove(test_file)

                return path
            except:
                self.conversation.newline()
                self.conversation.type(
                    "    Well this is embarrassing. I cannot write to that path.\n"
                )
                self.conversation.newline()

        raise RuntimeError

    def ask_for_value(self, name, current_value):
        value = input(f"{name} [{current_value}]: > ")
        if value in [None, ""]:
            return current_value

        return value

    def __check_for_configuration_migration(self):
        try:
            with open(self.paths.config, "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return self

        self.settings = json.loads(contents)
        if self.settings is None:
            return self

        for project_name, conf in self.settings.items():
            if "version" not in conf["meta"]:
                # -- Migrate from version 0 -> 1
                self.conversation.newline()
                self.conversation.type(
                    f"[MIGRATION] {project_name} configuration: 0 -> 1"
                )

                conf["meta"]["version"] = 1
                conf["dev"] = conf["copilot"]
                del conf["copilot"]

                self.settings[project_name] = conf

            if conf["meta"]["version"] == 1:
                # -- Migrate from version 1 -> 2
                self.conversation.newline()
                self.conversation.type(
                    f"[MIGRATION] {project_name} configuration: 1 -> 2\n"
                )
                self.conversation.type(
                    "  We advise that you execute the following command to "
                    + "configure new features:\n"
                    + "    gibson dev on\n"
                )
                self.conversation.wait()

                conf["meta"]["version"] = self.VERSION
                conf["dev"]["api"] = {"path": None, "prefix": "-", "version": "v1"}
                conf["dev"]["base"] = {"path": conf["dev"]["path"]["base"]}
                conf["dev"]["model"] = {"path": conf["dev"]["path"]["model"]}
                conf["dev"]["schema"] = {"path": conf["dev"]["path"]["schema"]}

                del conf["dev"]["path"]

                self.settings[project_name] = conf

            if conf["meta"]["version"] == 2:
                if "id" not in conf:
                    # Add the project ID and make it the first key in the project config
                    conf = dict({"id": None}, **conf)
                    self.settings[project_name] = conf

        self.write_config()

        return self

    def create_project_memory(self):
        self.require_project()
        try:
            os.makedirs(self.project.paths.memory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def display_project(self):
        project_name = "[None]"
        if self.project is not None:
            project_name = self.project.name

        self.conversation.display_project(project_name)

    def get_access_token(self):
        try:
            with open(f"{self.paths.auth}/{self.API_ENV}", "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return None

        token = json.loads(contents)
        return token["access_token"]

    def get_my_settings(self):
        self.require_project()
        return self.settings[self.project.name]

    def get_refresh_token(self):
        try:
            with open(f"{self.paths.auth}/{self.API_ENV}", "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return None

        token = json.loads(contents)
        return token["refresh_token"]

    def initialize(self):
        self.conversation.message_welcome()

        authenticated = self.login()
        if authenticated is False:
            self.conversation.message_login_failure()
            exit(1)
        else:
            self.conversation.message_login_success()

        self.conversation.message_project_setup()
        project_name = self.conversation.prompt_project()
        project_description = self.conversation.prompt_project_description(project_name)

        self.conversation.message_new_project(project_name)
        self.conversation.pause()

        section = self.append_project_to_conf(project_name, project_description)
        self.set_project_env(project_name)
        self.setup_project()
        self.create_project_memory()

        self.conversation.message_configuration_added(self.paths.config, section)
        self.conversation.wait()
        self.conversation.message_customize_settings()

        self.conversation.wait()
        self.conversation.message_environment()

        self.conversation.wait()
        self.conversation.message_explain_help()
        self.conversation.pause()
        print("")

        return self

    def login(self):
        server = AuthServer(self.app_domain())

        self.conversation.newline()
        self.conversation.type("We're opening your web browser to the login page.\n")
        self.conversation.type("Please log in and then return to this window.\n")
        self.conversation.newline()
        self.conversation.type(
            "If your browser does not open automatically, visit this URL:\n"
        )
        self.conversation.type(f"{server.get_url()}\n")

        access_token, refresh_token = server.get_tokens()
        if access_token is None or refresh_token is None:
            return False

        self.set_auth_tokens(access_token, refresh_token)
        return True

    def read_config(self):
        try:
            with open(self.paths.config, "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return self

        self.settings = json.loads(contents)

        return self

    def require_login(self):
        if self.get_access_token() is None:
            self.conversation.message_login_required(self)
            exit(1)

        return self

    def require_project(self):
        if self.project is None:
            self.conversation.gibsonai_project_not_set(self)
            exit(1)

        if self.project.name not in self.settings:
            self.conversation.unrecognized_project(self, self.project.name)
            exit(1)

        return self

    def require_project_key_or_id(self):
        if self.project.id:
            return self

        if not self.project.api.key or self.project.api.key == "FIXME":
            self.conversation.project_api_key_not_set(self)
            exit(1)

        return self

    def set_auth_tokens(self, access_token, refresh_token):
        try:
            os.mkdir(self.paths.auth)
        except FileExistsError:
            pass

        with open(f"{self.paths.auth}/{self.API_ENV}", "w") as f:
            data = {"access_token": access_token, "refresh_token": refresh_token}
            json.dump(data, f, indent=2)
            f.write("\n")

    def set_config_paths(self):
        config_path = os.environ.get("GIBSONAI_CONFIG_PATH", None)
        gibson_config_dir = ".gibsonai"
        user_home = os.environ.get("HOME")
        if user_home is None:
            raise RuntimeError(
                "Gibson here. Please set your HOME environment variable."
            )

        self.paths.top = config_path or f"{user_home}/{gibson_config_dir}"
        self.paths.auth = f"{self.paths.top}/auth"
        self.paths.config = f"{self.paths.top}/config"

    def set_project_env(self, project_name):
        os.environ["GIBSONAI_PROJECT"] = project_name
        return self

    def setup_project(self):
        config = None
        if self.settings is not None and len(self.settings.keys()) == 1:
            config = list(self.settings.values())[0]
            self.project = Project()
            self.project.name = list(self.settings.keys())[0]
        elif self.settings is not None:
            gibsonai_project = os.environ.get("GIBSONAI_PROJECT")
            if gibsonai_project is None:
                # TODO: traverse fs and attempt to find a .gibsonai/config file to use
                pass

            if gibsonai_project is not None:
                self.project = Project()
                self.project.name = gibsonai_project
                config = self.settings[gibsonai_project]

        if config is None or self.project is None:
            return self

        self.project.id = config.get("id")
        self.project.api.key = config["api"]["key"]
        self.project.code.custom.model_class = config["code"]["custom"]["model"][
            "class"
        ]
        self.project.code.custom.model_path = config["code"]["custom"]["model"]["path"]
        self.project.code.frameworks.api = config["code"]["frameworks"]["api"]
        self.project.code.frameworks.model = config["code"]["frameworks"]["model"]
        self.project.code.frameworks.revision = config["code"]["frameworks"]["revision"]
        self.project.code.frameworks.schema = config["code"]["frameworks"]["schema"]
        self.project.code.frameworks.test = config["code"]["frameworks"]["test"]
        self.project.code.language = config["code"]["language"]
        self.project.dev.active = config["dev"]["active"]
        self.project.dev.api.path = config["dev"]["api"]["path"]
        self.project.dev.api.prefix = config["dev"]["api"]["prefix"]
        self.project.dev.api.version = config["dev"]["api"]["version"]
        self.project.dev.base.path = config["dev"]["base"]["path"]
        self.project.dev.model.path = config["dev"]["model"]["path"]
        self.project.dev.schema.path = config["dev"]["schema"]["path"]
        self.project.datastore.type = config["datastore"]["type"]
        self.project.datastore.uri = config["datastore"]["uri"]
        self.project.description = config["meta"]["project"]["description"]
        self.project.modeler.version = config["modeler"]["version"]

        # TODO: needs to be fetched from project configuration
        config_path = os.environ.get("GIBSONAI_CONFIG_PATH", None)
        if config_path is None:
            config_path = self.paths.top

        self.project.paths.top = config_path
        self.project.paths.memory = f"{self.project.paths.top}/memory"
        self.project.paths.config = f"{self.project.paths.top}/config"

        return self

    def turn_dev_off(self):
        self.require_project()
        self.settings[self.project.name]["dev"]["active"] = False
        self.write_config()
        self.setup_project()
        return self

    def turn_dev_on(
        self, api_path, api_prefix, api_version, base_path, model_path, schema_path
    ):
        self.require_project()
        self.settings[self.project.name]["dev"]["active"] = True
        self.settings[self.project.name]["dev"]["api"]["path"] = api_path
        self.settings[self.project.name]["dev"]["api"]["prefix"] = api_prefix
        self.settings[self.project.name]["dev"]["api"]["version"] = api_version
        self.settings[self.project.name]["dev"]["base"]["path"] = base_path
        self.settings[self.project.name]["dev"]["model"]["path"] = model_path
        self.settings[self.project.name]["dev"]["schema"]["path"] = schema_path
        self.write_config()
        self.setup_project()
        return self

    def write_config(self):
        try:
            os.mkdir("/".join(self.paths.config.split("/")[0:-1]))
        except FileExistsError:
            pass

        with open(self.paths.config, "w") as f:
            json.dump(self.settings, f, indent=2)
            f.write("\n")

        self.read_config()

        return self
