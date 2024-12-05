import threading

from pathlib import Path
from tclogger import get_now_str
from typing import Literal, Union


MSG_PREFIXES = {"note": ">", "error": "×", "success": "✓"}


class FileLogger:
    def __init__(self, log_path: Union[str, Path], lock: threading.Lock = None):
        if not isinstance(log_path, Path):
            log_path = Path(log_path)
        self.log_path = log_path
        if not self.log_path.parent.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = lock or threading.Lock()

    def log(
        self,
        msg: str,
        msg_type: Literal["note", "error", "success"] = "note",
        add_now: bool = True,
    ):
        prefix = MSG_PREFIXES.get(msg_type, ">")
        if add_now:
            line = f"{prefix} [{get_now_str()}] {msg}\n"
        else:
            line = f"{prefix} {msg}\n"
        with self.lock:
            with open(self.log_path, "a") as f:
                f.write(line)
