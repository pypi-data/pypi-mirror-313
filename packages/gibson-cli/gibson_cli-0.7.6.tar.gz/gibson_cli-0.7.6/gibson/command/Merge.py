from gibson.command.BaseCommand import BaseCommand


class Merge(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        self.configuration.display_project()

        if self.memory.last is None or "entities" not in self.memory.last:
            self.conversation.type("No bueno. There is nothing to merge.\n\n")
            exit(1)

        if self.memory.entities is None:
            self.memory.entities = []

        entity_map = {}
        for i in range(len(self.memory.entities)):
            entity_map[self.memory.entities[i]["name"]] = i

        for entity in self.memory.last["entities"]:
            if entity["name"] not in entity_map:
                self.memory.entities.append(entity)
            else:
                self.memory.entities[entity_map[entity["name"]]] = entity

            self.conversation.type(f"[Merged] {entity['name']}\n")

        self.memory.remember_entities(self.memory.entities)
        self.memory.forget_last()
        self.memory.last = None

        self.conversation.newline()
