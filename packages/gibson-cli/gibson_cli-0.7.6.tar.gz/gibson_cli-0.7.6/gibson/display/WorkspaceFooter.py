import gibson.core.Colors as Colors


class WorkspaceFooter:
    def render(self):
        return (
            "-" * 79
            + "\n"
            + f"[{Colors.red(':q')} + enter = {Colors.red('discard')} changes]        "
            + f"[{Colors.green(':wq')} + enter = {Colors.green('save')} changes + write code]\n\n"
            + "Using natural language, tell me how I can modify this entity:"
        )
