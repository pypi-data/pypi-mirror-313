from dektools.serializer.pickaxe import dump, load

if __name__ == '__main__':
    _obj = {
        10: 0,
        11: 1,
        20: 0.,
        21: 1.,
        30: "",
        31: "test",
        32: "##########",
        33: "测试",
        300: b'',
        301: b'123',
        40: [],
        41: [1, 2],
        50: range(0),
        51: range(1),
        60: set(),
        61: {1, 2},
        71: {},
        72: {1: 2, 3: 4},
        73: True,
        74: False,
        "test": [],
        b'32': {2, 3}
    }
    _s = dump(_obj)
    print(_s)
    obj = load(_s)
    print(obj)

    obj = [obj, obj, {b'test': obj}]
    print(obj)
    s = dump(obj)
    obj_new = load(s)
    print(obj_new)
    assert dump(obj) == dump(obj_new)
