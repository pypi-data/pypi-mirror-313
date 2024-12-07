import os
import platform
import subprocess


class Platform:
    def __init__(self):
        self.system = platform.system().lower()

    def cmd_clear(self):
        if self.system == "windows":
            os.system("cls")
        else:
            subprocess.call("/usr/bin/clear")

        return self
