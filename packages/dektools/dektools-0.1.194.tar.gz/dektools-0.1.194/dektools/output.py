import sys
import json


class ToStrJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return repr(o)


def obj2str(obj):
    return json.dumps(obj, indent=4, ensure_ascii=False, sort_keys=True, cls=ToStrJSONEncoder)


def get_data_or_value(data, expression=None):
    if expression:
        from jsonpath_ng import parse
        rl = parse(expression).find(data)
        if rl:
            result = rl[0].value
        else:
            result = None
        if isinstance(result, (dict, list)):
            v = obj2str(result)
        else:
            v = str(result)
    else:
        v = obj2str(data)
    return v


def pprint(obj, *args, **kwargs):
    print(obj2str(obj), *args, **kwargs)


def print_data_or_value(data, expression=None):
    sys.stdout.write(get_data_or_value(data, expression))
    sys.stdout.flush()
