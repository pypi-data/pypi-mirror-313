import gibson.core.Colors as Colors
from gibson.display.WorkspaceFooter import WorkspaceFooter


def test_render():
    assert WorkspaceFooter().render() == (
        f"""-------------------------------------------------------------------------------
[{Colors.red(':q')} + enter = {Colors.red('discard')} changes]        [{Colors.green(':wq')} + enter = {Colors.green('save')} changes + write code]

Using natural language, tell me how I can modify this entity:"""
    )
