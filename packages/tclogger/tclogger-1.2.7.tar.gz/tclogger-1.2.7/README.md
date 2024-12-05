# tclogger
Python terminal colored logger

![](https://img.shields.io/pypi/v/tclogger?label=tclogger&color=blue&cacheSeconds=60)

## Install
```sh
pip install tclogger --upgrade
```

## Usage

Run example:

```sh
python example.py
```

See: [example.py](https://github.com/Hansimov/tclogger/blob/main/example.py)

```python
import sys
import tclogger
import time

from datetime import timedelta
from zoneinfo import ZoneInfo

from tclogger import TCLogger, logger, TCLogstr, logstr, colored, decolored
from tclogger import Runtimer, OSEnver, shell_cmd
from tclogger import get_now_ts, get_now_str, get_now_ts_str
from tclogger import TIMEZONE, set_timezone, tcdatetime
from tclogger import ts_to_str, str_to_ts, dt_to_str, unify_ts_and_str
from tclogger import CaseInsensitiveDict, dict_to_str, dict_get, dict_set
from tclogger import FileLogger
from tclogger import TCLogbar, TCLogbarGroup
from tclogger import brk, brc, brp
from tclogger import int_bits, max_key_len, chars_len
from tclogger import chars_slice


def test_logger_verbose():
    logger.note("Hello ", end="")
    logger.warn("You should not see this message", verbose=False)
    logger.mesg("World")
    logger.verbose = False
    logger.warn("You should not see later messages")
    logger.verbose = True
    logger.set_indent(2)
    logger.success("You should see this message, with indent")


def test_run_timer_and_logger():
    with Runtimer():
        logger.note(tclogger.__file__)
        logger.mesg(get_now_ts())
        logger.success(get_now_str())
        logger.note(f"Now: {logstr.mesg(get_now_str())}, ({logstr.file(get_now_ts())})")


def test_now_and_timezone():
    # Asia/Shanghai
    logger.success(TIMEZONE)
    logger.success(get_now_str())
    dt = tcdatetime.fromisoformat("2024-10-31")
    logger.success(dt)
    # Europe/London
    set_timezone("Europe/London")
    logger.note(get_now_str())
    dt = tcdatetime(year=2024, month=10, day=31)
    logger.note(dt)
    logger.note(tcdatetime.strptime("2024-10-31", "%Y-%m-%d"))
    logger.note(tcdatetime.now())
    dt = tcdatetime.fromisoformat("2024-10-31")
    logger.note(dt)
    logger.note(dt.strftime("%Y-%m-%d %H:%M:%S"))
    # America/New_York
    set_timezone("America/New_York")
    logger.warn(get_now_str())
    dt = tcdatetime.fromisoformat("2024-10-31")
    logger.warn(dt)
    logger.warn(dt.astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"))
    # Asia/Shanghai
    set_timezone("Asia/Shanghai")
    logger.success(get_now_str())
    # Compare
    dt1 = tcdatetime.fromisoformat("2024-12-03 12:00:00")
    dt2 = tcdatetime(year=2024, month=12, day=4)
    dt3 = tcdatetime.max()
    logger.note(f"dt1: {dt1}, dt2: {dt2}, dt3: {dt3}")
    cp12 = "<" if dt1 < dt2 else ">"
    cp23 = "<" if dt2 < dt3 else ">"
    cp13 = "<" if dt1 < dt3 else ">"
    logger.success(f"dt1 {cp12} dt2; dt2 {cp23} dt3; dt1 {cp13} dt3")


def test_dt_to_str():
    dt1 = timedelta(seconds=12)
    logger.note(f"dt1: {logstr.success(dt_to_str(dt1))}")
    dt2 = timedelta(seconds=60 * 24 + 12)
    logger.note(f"dt2: {logstr.success(dt_to_str(dt2))}")
    dt3 = timedelta(seconds=3600 * 8 + 60 * 24 + 12)
    logger.note(f"dt3: {logstr.success(dt_to_str(dt3))}")
    dt4 = timedelta(seconds=3600 * 24 * 1 + 3600 * 8 + 60 * 24 + 12)
    logger.note(f"dt4: {logstr.success(dt_to_str(dt4))}")

    t_ts = 1700000000
    t_ts, t_str = unify_ts_and_str(t_ts)
    logger.mesg(f"t_ts: {logstr.success(t_ts)}, t_str: {logstr.success(t_str)}")
    t_str = "2021-08-31 08:53:20"
    t_ts, t_str = unify_ts_and_str(t_str)
    logger.mesg(f"t_ts: {logstr.success(t_ts)}, t_str: {logstr.success(t_str)}")


def test_color():
    s1 = colored("hello", color="green", bg_color="bg_red", fonts=["bold", "blink"])
    s2 = colored("world", color="red", bg_color="bg_blue", fonts=["bold", "underline"])
    s3 = colored(f"BEG {s1} __ {s2} END")
    logger.note(s3)
    logger.success(s3)
    s4 = decolored(logstr.success(s3))
    print(s4)


def test_case_insensitive_dict():
    d = CaseInsensitiveDict()
    d["Hello"] = "old world"
    print(d["hello"])
    print(d)
    d["hELLo"] = "New WORLD"
    print(d["HEllO"])
    print(d)


def test_dict_get_and_set():
    d = {
        "owner": {"name": "Alice", "mid": 12345},
        "tags": ["tag1", "tag2", "tag3"],
        "children": [
            {
                "owner": {"name": "Bob", "mid": 54321},
                "tags": ["tag4", "tag5", "tag6"],
            }
        ],
    }
    print(dict_get(d, "owner.name"))
    print(dict_get(d, ["children", 0, "owner", "mid"]))
    dict_set(d, "owner.name", "Alice2")
    print(d)
    dict_set(d, ["owner", "mid"], 56789)
    print(d)
    print(dict_get(d, "owner.none", default="NotExist"))
    dict_set(d, "owner.new", "NewValue")
    print(d)
    dict_set(d, ["children", 1, "owner", "name"], "Bob2")
    print(d)
    dict_set(d, ["tags", 3], "tagsX")
    print(d)


def test_dict_to_str():
    d = {
        "hello": "world",
        "now": get_now_str(),
        "list": [1, 2, 3, [4, 5], "6"],
        "nested": {"key1": "value1", "key2": "value2", "key_3": {"subkey": "subvalue"}},
    }
    s = dict_to_str(d, add_quotes=True, max_depth=1)
    logger.success(s)
    s = dict_to_str(d, add_quotes=False, is_colored=False, max_depth=0)
    print(s)


def test_file_logger():
    file_logger = FileLogger(Path(__file__).parent / "test.log")
    file_logger.log("This is an error message", "error")


def test_align_dict_list():
    data = {
        "_id": None,
        "view_avg": 15175,
        "view_maxn": [94092954, 86624275, 68368263, 57713196, 53493614],
        "view_percentile": [39, 152, 254, 539, 3032, 13602, 51956, 282149, 94092954],
        "coin_avg": 57,
        "coin_maxn": [3093375, 2021980, 1420923, 1354206, 1312931],
        "coin_percentile": [0, 0, 0, 1, 6, 24, 76, 682, 3093375],
        "danmaku_avg": 26,
        "danmaku_maxn": [762005, 365521, 349354, 335414, 334935],
        "danmaku_percentile": [0, 0, 0, 0, 2, 12, 57, 353, 762005],
        "percentiles": [0.2, 0.4, 0.5, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0],
        "sub_lists": {
            "sub1": [1, 2, 4, 5, 6],
            "sub2": [21, 2, 35, 43, 89],
            "sub3": ["a", "abc", "gh", "jkl", "qerq"],
            "sub4": ["x", "ef", "i", "mkns", "adfa"],
        },
    }
    print(dict_to_str(data, align_list=True))


def test_list_of_dicts():
    dict_data = {
        "list_of_lists": [[1, 2, 3], ["a", "b", "c"]],
        "list_of_dicts": [{"key1": "dict1"}, {"key2": "dict2", "key3": "dict3"}],
        "empty_list": [],
        "empty_dict": {},
    }
    print(dict_to_str(dict_data, align_list=True))
    print()
    list_data = [{"key1": "val1"}, {"key2": "val2"}, {"key10": "val10"}]
    print(dict_to_str(list_data, align_list=True))


def test_logbar():
    epochs = 3
    total = 1000000
    logbar = TCLogbar(
        total=total, show_datetime=False, flush_interval=0.1, grid_mode="symbol"
    )
    for epoch in range(epochs):
        for i in range(total):
            logbar.update(increment=1)
            logbar.set_head(f"[{epoch+1}/{epochs}]")
        logbar.grid_mode = "shade"
        logbar.set_desc("THIS IS A SO LONG DESC WHICH IS USED TO TEST LINE UP")
        logbar.reset()


def test_logbar_group():
    epochs = 3
    total = 100
    sub_total = 1000
    epoch_bar = TCLogbar(total=epochs)
    epoch_bar.set_desc(f"[0/{epochs}]")
    progress_bar = TCLogbar(total=total)
    sub_progress_bar = TCLogbar(total=sub_total)
    TCLogbarGroup([epoch_bar, progress_bar, sub_progress_bar], show_at_init=True)
    # TCLogbarGroup([epoch_bar, progress_bar, sub_progress_bar], show_at_init=False)
    # print("This is a noise line to test lazy blank prints of logbar group.")
    # epoch_bar.update(0)
    for epoch in range(epochs):
        for i in range(total):
            for j in range(sub_total):
                sub_progress_bar.update(1, desc=f"[{j+1}/{sub_total}]")
                time.sleep(0.01)
            sub_progress_bar.reset()
            progress_bar.update(1, desc=f"[{i+1}/{total}]")
        progress_bar.reset()
        epoch_bar.set_desc()
        epoch_bar.update(1, desc=f"[{epoch+1}/{epochs}]", flush=True)


def test_logbar_total():
    total = 500

    logbar = TCLogbar()
    for i in range(total):
        logbar.update(1)
        time.sleep(0.001)
    logbar.flush()
    print()

    logbar = TCLogbar(total=total)
    for i in range(total + 250):
        logbar.update(1)
        time.sleep(0.01)


def test_logbar_verbose():
    total = 1000
    logbar1 = TCLogbar(total=total, show_datetime=False, head="bar1", verbose=False)
    logger.note("> Here should NOT show bar1")
    for i in range(total):
        logbar1.update(1)
    print()

    logbar2 = TCLogbar(total=total, show_datetime=False, head="bar2", verbose=True)
    logger.note("> Here should show bar2")
    for i in range(total):
        logbar2.update(1)
    print()

    logger.note("> Here should NOT show bar1 and bar2")
    TCLogbarGroup([logbar1, logbar2], verbose=False)
    print()

    logger.note("> Here should show bar1 and bar2")
    TCLogbarGroup([logbar1, logbar2], verbose=True)
    print()


def test_decorations():
    text = "Hello World"
    logger.note(f"Brackets: {logstr.mesg(brk(text))}")
    logger.note(f"Braces  : {logstr.mesg(brc(text))}")
    logger.note(f"Parens  : {logstr.mesg(brp(text))}")


def test_math():
    texts = ["你好", "Hello", 12345, "你好，世界！", "Hello, World!", None, 0, ""]
    res = {}
    for text in texts:
        text_len = chars_len(text)
        res[text] = text_len
    key_max_len = max_key_len(res)
    for text, text_len in res.items():
        text_str = str(text) + " " * (key_max_len - chars_len(str(text)))
        text_len_str = logstr.mesg(brk(text_len))
        logger.note(f"{text_str} : {text_len_str}")


def test_str_slice():
    texts = ["你好我是小明", "Hello", 12345789, "你好，世界！", "Hello, World!", "X"]
    for text in texts:
        sliced_str = chars_slice(str(text), start=0, end=6)
        logger.note(f"{sliced_str}: {logstr.mesg(text)}")


if __name__ == "__main__":
    test_logger_verbose()
    test_run_timer_and_logger()
    test_now_and_timezone()
    test_dt_to_str()
    test_color()
    test_case_insensitive_dict()
    test_dict_get_and_set()
    test_dict_to_str()
    test_align_dict_list()
    test_list_of_dicts()
    test_file_logger()
    test_logbar()
    test_logbar_group()
    test_logbar_total()
    test_logbar_verbose()
    test_decorations()
    test_math()
    test_str_slice()
```