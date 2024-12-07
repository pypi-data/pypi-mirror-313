def get_bases_reduce(bases):
    bases_reduce = [1]
    for x in reversed(bases):
        bases_reduce.insert(0, bases_reduce[0] * x)
    return bases_reduce


def format_bases(x, bases_reduce, trans):
    result = ''
    for index, base in enumerate(bases_reduce):
        value = x // base
        x -= value * base
        r = trans(value, index, x, bases_reduce, result)
        if r is None:
            break
        else:
            result += r
    return result


def format_duration(x, names=None, bases=None, trans=None):
    def trans_default(v, i, *_):
        return f'{v}{names[i]}' if v else ''

    names = names or ['d ', 'h ', 'm ', 's ', 'ms']
    return format_bases(x, get_bases_reduce(bases or [24, 60, 60, 1000]), trans or trans_default)


def format_duration_hms(x):
    def trans(v, i, *_):
        return '%02d%s' % (v, ":" if i < 2 else "") if i < 3 else None

    return format_duration(x // 1000 * 1000, bases=[60, 60, 1000], trans=trans)


def format_file_size_iec(x, names=None, bases=None):
    def trans(v, i, r, br, ret):
        return None if ret else ('%.2f %s' % (v + r / br[i], names[i]) if v else '')

    names = names or ['Tib', 'Gib', 'Mib', 'Kib', 'B']
    return format_bases(x, get_bases_reduce(bases or [1024] * 4), trans)


def format_file_size(x, names=None, bases=None):
    def trans(v, i, r, br, ret):
        return None if ret else ('%.2f %s' % (v + r / br[i], names[i]) if v else '')

    names = names or ['TB', 'GB', 'MB', 'KB', 'B']
    return format_bases(x, get_bases_reduce(bases or [1000] * 4), trans)
