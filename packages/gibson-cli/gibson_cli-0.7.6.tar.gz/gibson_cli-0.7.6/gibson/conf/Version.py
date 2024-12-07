from importlib import metadata


class Version:
    num = metadata.version("gibson-cli")
