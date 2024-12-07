import binascii
from collections.abc import Sequence, Set, Mapping

__all__ = ['dump', 'load', 'normalize', 'update']


def dump(obj):
    return _dump(obj)


def load(s):
    return _load(s)[0]


# only the obj test by `type(obj) === type(normalize(obj))` can be set to dict-key
def normalize(obj):
    return load(dump(obj))


def update(types):
    return _type_cv.update(types)


class PickaxeException(Exception):
    pass


_encoding = 'utf-8'
_mark_sep = '#'
_fixed_func = hash  # or None

_type_cv = {
    'str': {
        'weight': -100,
        'mark': 's',
        'type': lambda x: isinstance(x, str),
        'dump': lambda x: _s2hex(x),
        'load': lambda x: _hex2s(x)
    },
    'bool': {
        'weight': -150,
        'mark': 'o',
        'type': lambda x: isinstance(x, bool),
        'dump': lambda x: '_' if x else '',
        'load': lambda x: True if x else False
    },
    'int': {
        'weight': -200,
        'mark': 'i',
        'type': lambda x: isinstance(x, int),
        'dump': lambda x: str(x),
        'load': lambda x: int(x)
    },
    'dict': {
        'weight': -300,
        'mark': 'd',
        'type': lambda x: isinstance(x, Mapping),
        'dump': lambda x: ''.join(
            [f'{_dump(k)}{_dump(x[k])}' for k in (sorted(x, key=_fixed_func) if _fixed_func else x)]),
        'load': lambda x: dict(_pairs(_load_serial(x)))
    },
    'list': {
        'weight': -400,
        'mark': 'l',
        'type': lambda x: not isinstance(x, (str, bytes)) and isinstance(x, (Sequence, Set)),
        'dump': lambda x: ''.join([_dump(y) for y in x]),
        'load': lambda x: _load_serial(x)
    },
    'none': {
        'weight': -500,
        'mark': 'n',
        'type': lambda x: x is None,
        'dump': lambda x: '',
        'load': lambda x: None
    },
    'float': {
        'weight': -600,
        'mark': 'f',
        'type': lambda x: isinstance(x, float),
        'dump': lambda x: str(x),
        'load': lambda x: float(x)
    },
    'bytes': {
        'weight': -700,
        'mark': 'b',
        'type': lambda x: isinstance(x, bytes),
        'dump': lambda x: _b2hex(x),
        'load': lambda x: _hex2b(x)
    }
}
_type_cv_sorted = sorted([(k, v) for k, v in _type_cv.items()], key=lambda x: x[-1]['weight'], reverse=True)


def _get_type(obj):
    for t, c in _type_cv_sorted:
        if c['type'](obj):
            return t
    raise PickaxeException(f'Unknown type [{type(obj)}]: {obj}')


def _dump(obj):
    t = _get_type(obj)
    x = _type_cv[t]['dump'](obj)
    return f"{_type_cv[t]['mark']}{len(x)}{_mark_sep}{x}"  # '{mark}{content_length}{sep}{content}'


def _load(s):
    for t, xx in _type_cv.items():
        mark = xx['mark']
        if s.startswith(mark) and "0" <= s[len(mark):len(mark) + 1] <= "9":
            index_sep = s.find(_mark_sep)
            length = int(s[len(mark):index_sep])
            index_content = index_sep + len(_mark_sep)
            content = s[index_content:index_content + length]
            return _type_cv[t]['load'](content), s[index_content + length:]  # (loaded obj, rest string)
    raise PickaxeException(f'Unknown load string: {s}')


def _load_serial(s):
    serial = []
    while s:
        obj, rest = _load(s)
        serial.append(obj)
        s = rest
    return serial


def _pairs(serial):
    return zip(serial[::2], serial[1::2])


def _b2hex(b):
    return binascii.b2a_hex(b).decode(_encoding)


def _hex2b(h):
    return binascii.a2b_hex(h)


def _s2hex(s):
    return _b2hex(s.encode(_encoding))


def _hex2s(h):
    return _hex2b(h).decode(_encoding)
