import platform

from gibson.conf.Platform import Platform


def test_system():
    assert Platform().system == platform.system().lower()
