import os

import pytest

from gibson.lang.Python import Python


def test_make_python_path_no_match():
    assert Python().make_python_path("/a/b/c") == "/a/b/c"


def test_make_python_path_match():
    last_pythonpath = os.environ["PYTHONPATH"]

    try:
        os.environ["PYTHONPATH"] = "/a/b/c:/d/e/f"
        assert Python().make_python_path("/a/b/c/g") is None
        assert Python().make_python_path("/d/e/f/h") is None
    finally:
        os.environ["PYTHONPATH"] = last_pythonpath


def test_define_python_path():
    last_pythonpath = os.environ["PYTHONPATH"]

    try:
        os.environ["PYTHONPATH"] = "/a/b/c:/d/e/f"
        assert Python().define_python_path(["/a/b/c", "/d/e/f"]) is None
        assert Python().define_python_path(["/g/h/i", "/j/k/l"]) == "/g/h/i:/j/k/l"
    finally:
        os.environ["PYTHONPATH"] = last_pythonpath


def test_make_import_path_exceptions():
    with pytest.raises(SystemExit) as e:
        Python().make_import_path("/a/b/c")

    assert e.value.code == 1


def test_make_import_path():
    last_pythonpath = os.environ["PYTHONPATH"]

    try:
        os.environ["PYTHONPATH"] = "/a/b/c"
        assert Python().make_import_path(None) is None
        assert Python().make_import_path("/a/b/c/services/base") == "services.base"
        assert Python().make_import_path("/a/b/c/services/base/model") == (
            "services.base.model"
        )
        assert Python().make_import_path("/a/b/c/services/base/schema") == (
            "services.base.schema"
        )
    finally:
        os.environ["PYTHONPATH"] = last_pythonpath


def test_make_import_path_match_on_top_level():
    last_pythonpath = os.environ["PYTHONPATH"]

    try:
        os.environ["PYTHONPATH"] = "/a/b/c"
        assert Python().make_import_path("/a/b/c") == ""
    finally:
        os.environ["PYTHONPATH"] = last_pythonpath
