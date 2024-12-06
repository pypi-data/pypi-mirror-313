import re

default_version_sep = '.'


def version_pattern(sep=default_version_sep):
    return f'[0-9]+{sep}[0-9]+{sep}[0-9]+'


def version_to_tuple(version, sep=default_version_sep):
    rs = re.search(version_pattern(sep), version)
    if rs:
        return tuple(int(x) for x in rs.group().split('.'))


def version_is_digits(version, sep=default_version_sep):
    return bool(re.search(version_pattern(sep), version))


def version_digits(version, sep=default_version_sep):
    return re.search(version_pattern(sep), version).group()


def version_is_release(version, sep=default_version_sep):
    rs = re.search(version_pattern(sep), version)
    if rs:
        last = rs.span()[-1]
        return not version[last:]
    return False


def version_sorted(versions, reverse=False, sep=default_version_sep):
    keys = {x: version_to_tuple(x, sep=sep) for x in versions}
    return sorted(keys, key=lambda x: keys[x], reverse=reverse)
