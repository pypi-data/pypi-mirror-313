from .maths import chars_len


def chars_slice(
    text: str,
    start: int = None,
    end: int = None,
    use_chars_len: bool = True,
    fill_char: str = " ",
) -> str:
    """Slice string with start and end, considering chars length"""
    if start is None:
        start = 0
    if end is None:
        end = len(text)

    if not use_chars_len:
        return text[start:end]

    if start < 0:
        start = len(text) + start
    if end < 0:
        end = len(text) + end + 1

    res_start_idx = None
    res_end_idx = None
    fill_left = ""
    fill_right = ""
    res = ""
    ch_start = 0
    ch_end = 0
    for ch in text:
        ch_end = ch_start + chars_len(ch)
        if ch_start >= start and ch_end <= end:
            res += ch
            if res_start_idx is None:
                res_start_idx = ch_start
                fill_left = fill_char * (ch_start - start)
        if ch_end >= end:
            if res_end_idx is None:
                res_end_idx = ch_end
                fill_right = fill_char * (ch_end - end)
            break
        ch_start = ch_end
    if res_end_idx is None:
        res_end_idx = ch_end
        fill_right = fill_char * (end - ch_end)
    res = fill_left + res + fill_right
    return res
