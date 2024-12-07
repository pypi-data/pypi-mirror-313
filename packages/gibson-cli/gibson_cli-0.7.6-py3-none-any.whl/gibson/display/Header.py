import math

from gibson.core.Colors import bold


class Header:
    def render(self, text, colorizer=None):
        output = text if colorizer is None else colorizer(text)
        half = math.floor((78 - len(text)) / 2)  # 80 line length - 2 spaces
        header = "/" * half + f" {bold(output)} " + "/" * half
        return header
