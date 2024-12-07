import json
import os

from gibson.core.Configuration import Configuration


class Memory:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.entities = None
        self.last = None
        self.bootstrap()

    def append_last(self, entity: dict):
        if self.last is None:
            self.last = {"entities": []}

        self.last["entities"].append(entity)
        self.remember_last(self.last)

        return self

    def bootstrap(self):
        if self.configuration.project is not None:
            self.__make_memory_dir()
            self.entities = self.recall_entities()
            self.last = self.recall_last()

    def __forget(self, file):
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

        return self

    def forget_entities(self):
        self.__forget(self.get_path_entities())
        return self

    def forget_last(self):
        self.__forget(self.get_path_last())
        return self

    def __recall(self, file):
        try:
            with open(file, "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return None

        return json.loads(contents)

    def recall_entities(self):
        return self.__recall(self.get_path_entities())

    def recall_entity(self, name):
        entity = self.recall_last_entity(name)
        if entity is not None:
            return entity

        entity = self.recall_stored_entity(name)
        if entity is not None:
            return entity

        return None

    def recall_last(self):
        return self.__recall(self.get_path_last())

    def recall_last_entity(self, name):
        if self.last is not None:
            for entity in self.last["entities"]:
                if entity["name"].lower() == name.lower():
                    return entity
        return None

    def recall_merged(self):
        if self.entities is None:
            if self.last is not None:
                return self.last["entities"]
            else:
                return []

        entities = []
        last_map = {}
        if self.last is not None:
            for entry in self.last["entities"]:
                last_map[entry["name"]] = True
                entities.append(entry)

        for entry in self.entities:
            if entry["name"] not in last_map:
                entities.append(entry)

        return entities

    def recall_stored_entity(self, name):
        if self.entities is not None:
            for entity in self.entities:
                if entity["name"].lower() == name.lower():
                    return entity

        return None

    def __remember(self, file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")

        return self

    def remember_entities(self, entities: list):
        self.__remember(self.get_path_entities(), entities)
        return self

    def remember_last(self, data: dict):
        self.__remember(self.get_path_last(), data)
        return self

    def get_path_entities(self):
        return self.get_path_top() + "/entities"

    def get_path_last(self):
        return self.get_path_top() + "/last"

    def get_path_top(self):
        return os.path.expandvars(
            self.configuration.project.paths.memory
            + "/"
            + self.configuration.project.name
        )

    def __make_memory_dir(self):
        try:
            os.mkdir(self.get_path_top())
        except FileExistsError:
            pass

    def stats(self):
        num_entities = len(self.entities) if self.entities is not None else 0
        num_last = len(self.last["entities"]) if self.last is not None else 0

        return {
            "entities": {"num": num_entities, "word": self.word_entities(num_entities)},
            "last": {"num": num_last, "word": self.word_entities(num_last)},
        }

    def word_entities(self, num):
        return "entities" if num == 0 or num > 1 else "entity"
