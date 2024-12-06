class MapChain:
    EMPTY = type('empty', (), {})

    def __init__(self, data=None, parents=None):
        self.parents = parents or []
        self.data = data or {}

    def __repr__(self):
        return repr(self.flat())

    def derive(self, data=None):
        return self.__class__(data=data, parents=[self])

    def dependency(self):
        self.parents = []

    def add_item(self, key, value):
        self.data[key] = value

    def update(self, data):
        for k, v in data.items():
            self.add_item(k, v)

    def get_item(self, key, default=EMPTY):
        value = self.data.get(key, self.EMPTY)
        if value is not self.EMPTY:
            return value
        for parent in self.parents:
            value = parent.get_item(key)
            if value is not self.EMPTY:
                return value
        if default is not self.EMPTY:
            return default
        raise ValueError(f"Can't find the key: {key}")

    def flat(self):
        def walk(node):
            nonlocal data
            data = node.data | data
            for parent in node.parents:
                walk(parent)

        data = {}
        walk(self)
        data_normal = {}
        delay_list = []
        for k, v in data.items():
            if isinstance(v, DelayMap):
                delay_list.append(v)
            else:
                data_normal[k] = v
        data_result = {}
        for delay in delay_list:
            data_result.update(delay.flat(data_normal))
        return data_normal | data_result


class DelayMap:
    def __init__(self, func):
        self.func = func

    def flat(self, data):
        return self.func(data)
