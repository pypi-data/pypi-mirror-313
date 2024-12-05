from typing import Union


class CaseInsensitiveDict(dict):
    """Inspired by: https://stackoverflow.com/a/32888599"""

    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(
            self.__class__._k(key), *args, **kwargs
        )

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(
            self.__class__._k(key), *args, **kwargs
        )

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(
            self.__class__._k(key), *args, **kwargs
        )

    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)


def dict_get(d: dict, keys: Union[str, list[str]], default=None, sep: str = "."):
    if isinstance(keys, str) and sep:
        keys = keys.split(sep)
    for key in keys:
        if (isinstance(d, dict) and key in d) or (isinstance(d, list) and key < len(d)):
            d = d[key]
        else:
            return default
    return d


def dict_set(d: dict, keys: Union[str, list[str]], value, sep: str = "."):
    if isinstance(keys, str) and sep:
        keys = keys.split(sep)
    for key in keys[:-1]:
        if isinstance(d, dict):
            d = d.setdefault(key, {})
        elif isinstance(d, list):
            if key >= len(d):
                d.extend([{} for _ in range(key - len(d) + 1)])
            d = d[key]

    if isinstance(d, dict):
        d[keys[-1]] = value
    elif isinstance(d, list):
        if keys[-1] >= len(d):
            d.extend([None for _ in range(keys[-1] - len(d) + 1)])
        d[keys[-1]] = value
