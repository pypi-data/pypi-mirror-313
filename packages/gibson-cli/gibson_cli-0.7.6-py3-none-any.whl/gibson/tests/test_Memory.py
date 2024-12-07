from gibson.core.Configuration import Configuration
from gibson.core.Memory import Memory


def test_recall_merged_no_entities():
    memory = Memory(Configuration())
    memory.entities = None
    memory.last = None

    assert memory.recall_merged() == []


def test_recall_merged_entities_only():
    memory = Memory(Configuration())
    memory.entities = [{"definition": "abc", "name": "def"}]
    memory.last = None

    assert memory.recall_merged() == [{"definition": "abc", "name": "def"}]


def test_recall_merged_last_only():
    memory = Memory(Configuration())
    memory.entities = None
    memory.last = {"entities": [{"definition": "abc", "name": "def"}]}

    assert memory.recall_merged() == [{"definition": "abc", "name": "def"}]


def test_recall_merged_no_overlap():
    memory = Memory(Configuration())
    memory.entities = [{"definition": "abc", "name": "def"}]
    memory.last = {"entities": [{"definition": "ghi", "name": "jkl"}]}

    assert memory.recall_merged() == [
        {"definition": "ghi", "name": "jkl"},
        {"definition": "abc", "name": "def"},
    ]


def test_recall_merged_overlap():
    memory = Memory(Configuration())
    memory.entities = [
        {"definition": "abc", "name": "def"},
        {"definition": "ghi", "name": "jkl"},
    ]
    memory.last = {
        "entities": [
            {"definition": "xyz", "name": "def"},
            {"definition": "mno", "name": "pqr"},
        ]
    }

    assert memory.recall_merged() == [
        {"definition": "xyz", "name": "def"},
        {"definition": "mno", "name": "pqr"},
        {"definition": "ghi", "name": "jkl"},
    ]


def test_recall_entity_none():
    memory = Memory(Configuration())
    memory.entities = None
    memory.last = None

    assert memory.recall_entity("abc") is None


def test_recall_entity_entities():
    memory = Memory(Configuration())
    memory.entities = [{"definition": "abc", "name": "def"}]
    memory.last = None

    assert memory.recall_entity("def") == {"definition": "abc", "name": "def"}


def test_recall_entity_last():
    memory = Memory(Configuration())
    memory.entities = None
    memory.last = {"entities": [{"definition": "abc", "name": "def"}]}

    assert memory.recall_entity("def") == {"definition": "abc", "name": "def"}


def test_recall_entity_prefer_last():
    memory = Memory(Configuration())
    memory.entities = [{"definition": "abc", "name": "def"}]
    memory.last = {"entities": [{"definition": "xyz", "name": "def"}]}

    assert memory.recall_entity("def") == {"definition": "xyz", "name": "def"}
