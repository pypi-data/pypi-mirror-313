class Constants:
    BLACK = "\033[30m"
    BLACK_BG = "\033[40m"
    BLINK = "\033[5m"
    BLINK2 = "\033[6m"
    BLUE = "\033[34m"
    BLUE_BG = "\033[44m"
    BLUE_BG2 = "\033[104m"
    BLUE2 = "\033[94m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    CYAN_BG = "\033[46m"
    CYAN_BG2 = "\033[106m"
    CYAN2 = "\033[96m"
    END = "\033[0m"
    GREEN = "\033[32m"
    GREEN_BG = "\033[42m"
    GREEN_BG2 = "\033[102m"
    GREEN2 = "\033[92m"
    GREY = "\033[90m"
    GREY_BG = "\033[100m"
    ITALIC = "\033[3m"
    RED = "\033[31m"
    RED_BG = "\033[41m"
    RED_BG2 = "\033[101m"
    RED2 = "\033[91m"
    SELECTED = "\033[7m"
    UNDERLINE = "\033[4m"
    VIOLET = "\033[35m"
    VIOLET_BG = "\033[45m"
    VIOLET_BG2 = "\033[105m"
    VIOLET2 = "\033[95m"
    WHITE = "\033[37m"
    WHITE_BG = "\033[47m"
    WHITE_BG2 = "\033[107m"
    WHITE2 = "\033[97m"
    YELLOW = "\033[33m"
    YELLOW_BG = "\033[43m"
    YELLOW_BG2 = "\033[103m"
    YELLOW2 = "\033[93m"


# Colorize text with a given color
def colorize(text, color):
    return f"{color}{text}{Constants.END}"


# Colorize a command
def command(
    command,
    sub=None,
    args=None,
    inputs=None,
    hint=None,
):
    parts = [green(command)]
    if sub:
        parts.append(subcommand(sub))
    if args:
        if isinstance(args, list):
            parts.append(arguments(args))
        else:
            parts.append(argument(args))
    if inputs:
        if isinstance(inputs, list):
            for input_ in inputs:
                parts.append(user_input(input_))
        else:
            parts.append(user_input(inputs))
    if hint:
        parts.append(grey(hint))
    return " ".join(parts)


# Colorize a subcommand
def subcommand(text):
    return yellow(text)


# Colorize an argument
def argument(text):
    return violet(text)


# Colorize a list of arguments
def arguments(list):
    return f"[{'|'.join(map(lambda x: argument(x), list))}]"


# Colorize user input
def user_input(text):
    return white(text)


# Colorize a command option
def option(text):
    return cyan(text)


# Colorize a hint
def hint(text):
    return grey(text)


# Colorize a project name
def project(text):
    return bold(text)


# Colorize a URL to appear as a link
def link(text):
    return underline(blue(text))


# Colorize an entity name
def entity(text):
    return bold(violet(text))


# Colorize the table name in a SQL statement
def table(sql, name):
    return sql.replace(name, entity(name), 1)


# Colorize the table name in model code
def model(code, model_name, entity_name):
    return code.replace(model_name, entity(model_name), 1).replace(
        f'__tablename__ = "{entity_name}"', f'__tablename__ = "{entity(entity_name)}"'
    )


# Colorize a time/duration output
def time(text):
    return green(text)


def bold(text):
    return colorize(text, Constants.BOLD)


def underline(text):
    return colorize(text, Constants.UNDERLINE)


def blue(text):
    return colorize(text, Constants.BLUE)


def cyan(text):
    return colorize(text, Constants.CYAN)


def green(text):
    return colorize(text, Constants.GREEN)


def grey(text):
    return colorize(text, Constants.GREY)


def red(text):
    return colorize(text, Constants.RED)


def violet(text):
    return colorize(text, Constants.VIOLET)


def white(text):
    return colorize(text, Constants.WHITE2)


def yellow(text):
    return colorize(text, Constants.YELLOW)
