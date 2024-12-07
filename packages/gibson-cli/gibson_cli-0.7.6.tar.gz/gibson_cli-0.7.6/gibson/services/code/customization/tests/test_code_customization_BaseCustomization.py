import pytest

from gibson.core.Configuration import Configuration
from gibson.services.code.customization.BaseCustomization import BaseCustomization


def test_preserve_exception():
    with pytest.raises(NotImplementedError):
        BaseCustomization(Configuration()).preserve()


def test_restore_exception():
    with pytest.raises(NotImplementedError):
        BaseCustomization(Configuration()).restore()
