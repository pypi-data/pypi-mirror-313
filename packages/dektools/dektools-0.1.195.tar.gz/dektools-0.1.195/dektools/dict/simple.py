import json
import typing
from collections import OrderedDict


def assign(*args, cls=dict):
    result = cls()
    dict_merge(result, *args)
    return result


def dict_merge(dct, *args):
    for arg in args:
        _dict_merge(dct, arg)


def _dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if is_dict(dct.get(k)) and is_dict(merge_dct[k]):
            _dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def list_dedup(array):
    return array.__class__(OrderedDict.fromkeys(array))


def is_list(x):
    return isinstance(x, (list, tuple))


def is_dict(x):
    return isinstance(x, typing.Mapping)


def apply(tmpl, data):
    if is_list(data):
        if is_list(tmpl):
            result = []
            if len(tmpl) > 1:
                t = tmpl[0]
            else:
                t = {}
            for x in data:
                result.append(apply(t, x))
            return result
        else:
            return data
    elif is_dict(data):
        if is_dict(tmpl) and not is_list(tmpl):
            result = data.__class__()
            for k in data:
                result[k] = apply(tmpl[k], data[k]) if k in tmpl else data[k]
            for k in tmpl:
                if k not in result:
                    v = tmpl[k]
                    if is_list(v) and len(v) == 1 and is_dict(v[0]):
                        v = []
                    result[k] = v
            return result
        else:
            return data
    else:
        return data


def assign_flex(*args, cls=dict):
    result = cls()
    for arg in args:
        merge_flex(result, arg)
    return result


_merge_suffix = '__merge_flex'
_merge_options = {'prev', 'post', 'default', 'tmpl', 'cover'}


def key_of_merge_flex(k):
    return f'{k}{_merge_suffix}'


def merge_flex(dct, merge_dct, operation=None):
    for k in merge_dct:
        if k.endswith(_merge_suffix):
            continue
        if k not in dct:
            dct[k] = merge_dct[k]
            continue
        data, data2 = dct.get(k), merge_dct[k]
        operation_ = merge_dct.get(key_of_merge_flex(k)) or operation or 'default'
        if operation_ == 'tmpl':
            dct[k] = apply(data, data2)
        elif operation_ == 'cover':
            dct[k] = data2
        else:
            if operation_ == 'prev':
                data, data2 = data2, data
            if is_list(data):
                if operation_ == 'default':
                    dct[k] = data2
                else:
                    if is_list(data2):
                        dct[k] = [*data, *data2]
                    else:
                        dct[k] = [*data, data2]
            else:
                if is_dict(data) and is_dict(data2):
                    merge_flex(data, data2)
                else:
                    dct[k] = data2


def sorted_dict(data, key=None):
    key = key or (lambda d: sorted(d.keys()))
    return OrderedDict([(k, data[k]) for k in key(data)])


def assign_list(a, b):
    result = []
    length = max(len(a), len(b))
    for i in range(length):
        value = None
        if i < len(a):
            value = a[i]
        if i < len(b):
            value = b[i]
        result.append(value)
    return result


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def string_to_map_list(s, sep=None):
    sep = sep or [';', ',']
    result = {}
    for item in s.split(sep[0]):
        item = item.strip()
        if item:
            key, values = item.split(':', 1)
            array = result[key] = []
            for value in values.split(sep[1]):
                value = value.strip()
                if value:
                    array.append(value)
    return result


def normal_weights(weights):
    result = {}
    cursor = 0
    last = None
    for key in sorted(weights, key=lambda x: weights[x]):
        if last is not None:
            if weights[last] != weights[key]:
                cursor += 1
        result[key] = cursor
        last = key
    return result


if __name__ == '__main__':
    print(normal_weights({'a': 0, 'b': 1, 'c': 1, 'd': 2}) == {'a': 0, 'b': 1, 'c': 1, 'd': 2})
