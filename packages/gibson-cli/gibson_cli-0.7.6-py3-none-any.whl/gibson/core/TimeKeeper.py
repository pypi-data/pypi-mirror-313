import time

import gibson.core.Colors as Colors


class TimeKeeper:
    def __init__(self):
        self.__started = time.time()

    def display(self):
        print(self.get_display() + "\n")

    def get_display(self):
        return Colors.time("[%ss]" % str(time.time() - self.__started)[0:7])
