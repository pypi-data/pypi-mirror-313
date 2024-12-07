from difflib import Differ

from gibson.core.Colors import green, red


# Highlights all lines as additions with a green + at the beginning
# This keeps visual clutter to a minimum when showing the diff of an entirely new entity
def additions(input: str):
    lines = input.splitlines(keepends=True)
    result = []
    for line in lines:
        result.append(f"{green('+')} {line}")
    return "".join(result)


# Highlights the diffs between two strings, showing the additions and removals as distinct colored lines
def diff(original: str, modified: str):
    diffs = list(
        Differ().compare(
            original.splitlines(keepends=True), modified.splitlines(keepends=True)
        )
    )

    result = []
    for line in diffs:
        if line.startswith("+ "):
            result.append(green(line))
        elif line.startswith("- "):
            result.append(red(line))
        elif line.startswith("  "):
            result.append(line)
        # Ignore lines starting with '? ' as they are not needed for this highlighting

    return "".join(result)
