import os
import shutil

from gibson.core.Configuration import Configuration
from gibson.services.code.customization.Authenticator import Authenticator


def test_link_target():
    configuration = Configuration()
    configuration.project.dev.api.path = "/tmp/gibsonai-unit-test"
    configuration.project.dev.api.version = "v1"

    try:
        os.makedirs("/tmp/gibsonai-unit-test/v1")

        os.symlink("/etc/passwd", "/tmp/gibsonai-unit-test/v1/Authenticator.py")

        authenticator = Authenticator(configuration).preserve()
        os.unlink("/tmp/gibsonai-unit-test/v1/Authenticator.py")
        authenticator.restore()

        assert os.path.islink("/tmp/gibsonai-unit-test/v1/Authenticator.py") is True
        assert os.readlink("/tmp/gibsonai-unit-test/v1/Authenticator.py") == (
            "/etc/passwd"
        )
    finally:
        shutil.rmtree("/tmp/gibsonai-unit-test")


def test_file_contents():
    configuration = Configuration()
    configuration.project.dev.api.path = "/tmp/gibsonai-unit-test"
    configuration.project.dev.api.version = "v1"

    try:
        os.makedirs("/tmp/gibsonai-unit-test/v1")

        with open("/tmp/gibsonai-unit-test/v1/Authenticator.py", "w") as f:
            f.write("abc def\nghi jkl")

        authenticator = Authenticator(configuration).preserve()
        os.unlink("/tmp/gibsonai-unit-test/v1/Authenticator.py")
        assert os.path.islink("/tmp/gibsonai-unit-test/v1/Authenticator.py") is False
        assert os.path.isfile("/tmp/gibsonai-unit-test/v1/Authenticator.py") is False
        authenticator.restore()

        assert os.path.islink("/tmp/gibsonai-unit-test/v1/Authenticator.py") is False
        assert os.path.isfile("/tmp/gibsonai-unit-test/v1/Authenticator.py") is True

        with open("/tmp/gibsonai-unit-test/v1/Authenticator.py", "r") as f:
            assert f.read() == "abc def\nghi jkl"
    finally:
        shutil.rmtree("/tmp/gibsonai-unit-test")
