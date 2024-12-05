"""Math utils"""

import math
from typing import Union


def int_bits(num, base: int = 10):
    """Calc bits of integer with base X"""
    return math.ceil(math.log(num + 1, base))


def chars_len(chars: Union[str, int]) -> int:
    """Calc length of chars"""
    chars = str(chars)
    res = 0
    if isinstance(chars, int):
        chars = str(chars)
    for ch in chars:
        if ord(ch) > 255:
            res += 2
        else:
            res += 1
    return res


def max_key_len(d: dict, offset: int = 0, use_chars_len: bool = True) -> int:
    """Get max string length of dict keys"""
    if not d:
        return 0
    len_func = chars_len if use_chars_len else len
    return max([len_func(str(k)) + offset for k in d.keys()])
