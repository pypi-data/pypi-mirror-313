from gibson.command.BaseCommand import BaseCommand
from gibson.core.Configuration import Configuration


def test_customization_management():
    command = BaseCommand(Configuration())

    assert command.customization_management_is_enabled() is True
    command.disable_customization_management()
    assert command.customization_management_is_enabled() is False
