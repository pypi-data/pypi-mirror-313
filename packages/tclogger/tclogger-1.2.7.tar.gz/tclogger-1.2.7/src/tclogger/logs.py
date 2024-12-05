"""Logger utils"""

import functools
import inspect
import logging
import shutil

from .colors import colored, decolored, COLOR_TYPE


def add_fillers(
    text: str,
    filler: str = "=",
    fill_side: str = "both",
    is_text_colored: bool = False,
    fill_color: COLOR_TYPE = None,
):
    terminal_width = shutil.get_terminal_size().columns
    text = text.strip()
    if is_text_colored:
        text_width = len(decolored(text))
    else:
        text_width = len(text)
    if text_width >= terminal_width:
        return text

    if fill_side[0].lower() == "b":
        leading_fill_str = filler * ((terminal_width - text_width) // 2 - 1) + " "
        trailing_fill_str = " " + filler * (
            terminal_width - text_width - len(leading_fill_str) - 1
        )
    elif fill_side[0].lower() == "l":
        leading_fill_str = filler * (terminal_width - text_width - 1) + " "
        trailing_fill_str = ""
    elif fill_side[0].lower() == "r":
        leading_fill_str = ""
        trailing_fill_str = " " + filler * (terminal_width - text_width - 1)
    else:
        raise ValueError("Invalid fill_side")

    if fill_color:
        leading_fill_str = colored(leading_fill_str, color=fill_color)
        trailing_fill_str = colored(trailing_fill_str, color=fill_color)

    filled_str = f"{leading_fill_str}{text}{trailing_fill_str}"
    return filled_str


LOG_METHODS = {
    "err": ("error", "red"),
    "warn": ("warning", "light_red"),
    "hint": ("info", "light_yellow"),
    "note": ("info", "light_magenta"),
    "mesg": ("info", "light_cyan"),
    "file": ("info", "light_blue"),
    "line": ("info", "white"),
    "success": ("info", "light_green"),
    "fail": ("info", "light_red"),
    "back": ("debug", "light_cyan"),
}


class TCLogstr:
    def __init__(self):
        self.COLORS = {k: v[1] for k, v in LOG_METHODS.items()}

    def colored_str(self, msg, method, *args, **kwargs):
        return colored(msg, color=self.COLORS[method.lower()], *args, **kwargs)

    def err(self, msg: str = ""):
        return self.colored_str(msg, "err")

    def warn(self, msg: str = ""):
        return self.colored_str(msg, "warn")

    def hint(self, msg: str = ""):
        return self.colored_str(msg, "hint")

    def note(self, msg: str = ""):
        return self.colored_str(msg, "note")

    def mesg(self, msg: str = ""):
        return self.colored_str(msg, "mesg")

    def file(self, msg: str = ""):
        return self.colored_str(msg, "file")

    def line(self, msg: str = ""):
        return self.colored_str(msg, "line")

    def success(self, msg: str = ""):
        return self.colored_str(msg, "success")

    def fail(self, msg: str = ""):
        return self.colored_str(msg, "fail")

    def back(self, msg: str = ""):
        return self.colored_str(msg, "back")


logstr = TCLogstr()


class TCLogger(logging.Logger):
    INDENT_METHODS = [
        "indent",
        "set_indent",
        "reset_indent",
        "store_indent",
        "restore_indent",
        "log_indent",
    ]
    LEVEL_METHODS = [
        "set_level",
        "store_level",
        "restore_level",
        "quiet",
        "enter_quiet",
        "exit_quiet",
    ]
    LEVEL_NAMES = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }

    def __init__(self, name=None, prefix=False, verbose: bool = True):
        if not name:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            name = module.__name__

        super().__init__(name)
        self.setLevel(logging.INFO)
        self.verbose = verbose

        if prefix:
            formatter_prefix = "[%(asctime)s] - [%(name)s] - [%(levelname)s]\n"
        else:
            formatter_prefix = ""

        self.formatter = logging.Formatter(formatter_prefix + "%(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(self.formatter)
        self.addHandler(stream_handler)

        self.log_indent = 0
        self.log_indents = []

        self.log_level = "info"
        self.log_levels = []

    def indent(self, indent=2):
        self.log_indent += indent

    def set_indent(self, indent=2):
        self.log_indent = indent

    def reset_indent(self):
        self.log_indent = 0

    def store_indent(self):
        self.log_indents.append(self.log_indent)

    def restore_indent(self):
        self.log_indent = self.log_indents.pop(-1)

    def set_level(self, level):
        self.log_level = level
        self.setLevel(self.LEVEL_NAMES[level])

    def store_level(self):
        self.log_levels.append(self.log_level)

    def restore_level(self):
        self.log_level = self.log_levels.pop(-1)
        self.set_level(self.log_level)

    def quiet(self):
        self.set_level("critical")

    def enter_quiet(self, quiet=False):
        if quiet:
            self.store_level()
            self.quiet()

    def exit_quiet(self, quiet=False):
        if quiet:
            self.restore_level()

    def log(
        self,
        method,
        msg,
        indent=0,
        fill=False,
        fill_side="both",
        end="\n",
        verbose: bool = None,
        *args,
        **kwargs,
    ):
        verbose = self.verbose if verbose is None else verbose
        if not verbose:
            return

        if type(msg) == str:
            msg_str = msg
        else:
            msg_str = repr(msg)
            quotes = ["'", '"']
            if msg_str[0] in quotes and msg_str[-1] in quotes:
                msg_str = msg_str[1:-1]

        indent_str = " " * (self.log_indent + indent)
        indented_msg = "\n".join([indent_str + line for line in msg_str.split("\n")])

        if fill:
            indented_msg = add_fillers(indented_msg, fill_side=fill_side)

        handler = self.handlers[0]
        handler.terminator = end

        level, color = LOG_METHODS[method]
        getattr(self, level)(logstr.colored_str(indented_msg, method), *args, **kwargs)

    def route_log(self, method, msg, *args, **kwargs):
        level, color = LOG_METHODS[method]
        # if level is lower (less important) than self.log_level, do not log
        if self.LEVEL_NAMES[level] < self.LEVEL_NAMES[self.log_level]:
            return
        functools.partial(self.log, method, msg)(*args, **kwargs)

    def err(self, msg: str = "", *args, **kwargs):
        self.route_log("err", msg, *args, **kwargs)

    def warn(self, msg: str = "", *args, **kwargs):
        self.route_log("warn", msg, *args, **kwargs)

    def hint(self, msg: str = "", *args, **kwargs):
        self.route_log("hint", msg, *args, **kwargs)

    def note(self, msg: str = "", *args, **kwargs):
        self.route_log("note", msg, *args, **kwargs)

    def mesg(self, msg: str = "", *args, **kwargs):
        self.route_log("mesg", msg, *args, **kwargs)

    def file(self, msg: str = "", *args, **kwargs):
        self.route_log("file", msg, *args, **kwargs)

    def line(self, msg: str = "", *args, **kwargs):
        self.route_log("line", msg, *args, **kwargs)

    def success(self, msg: str = "", *args, **kwargs):
        self.route_log("success", msg, *args, **kwargs)

    def fail(self, msg: str = "", *args, **kwargs):
        self.route_log("fail", msg, *args, **kwargs)

    def back(self, msg: str = "", *args, **kwargs):
        self.route_log("back", msg, *args, **kwargs)


logger = TCLogger()
