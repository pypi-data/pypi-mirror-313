#!/usr/bin/env python3

from gibson.core.CommandRouter import CommandRouter
from gibson.core.Configuration import Configuration


def main():
    try:
        configuration = Configuration()
        if configuration.settings is None:
            configuration.initialize()
        else:
            CommandRouter(configuration).run()
    except KeyboardInterrupt:
        exit(1)


if __name__ == "__main__":
    main()
