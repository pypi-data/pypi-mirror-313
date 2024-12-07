import gibson.core.Colors as Colors
from gibson.display.WorkspaceHeader import WorkspaceHeader


def test_render():
    assert WorkspaceHeader().render("abc def ghi") == (
        f"""Project {Colors.project("abc def ghi")}                                             {Colors.bold("PAIR PROGRAMMER")}
-------------------------------------------------------------------------------"""
    )
