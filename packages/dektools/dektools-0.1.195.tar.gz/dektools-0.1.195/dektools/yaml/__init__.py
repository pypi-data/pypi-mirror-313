import os
import codecs
import yaml as pyyaml
import yamlloader
from io import BytesIO
from ..file import sure_dir, normal_path
from .tags import StrTag

DEFAULT_VALUE = type('default_value', (), {})


class Yaml:
    dump_kwargs = dict(
        allow_unicode=True,
        indent=2,
    )

    def __init__(self, resolvers, encoding=None):
        resolvers = Resolver.clone(resolvers)
        self.loder = resolvers[0]
        self.dumper = resolvers[1]
        self.encoding = encoding or "utf-8"
        self.register_list = []

    def register(self, cls):
        if cls.yaml_tag_multi:
            self.loder.add_multi_constructor(cls.yaml_tag, cls.from_yaml_multi)
        else:
            self.loder.add_constructor(cls.yaml_tag, cls.from_yaml)
        self.dumper.add_multi_representer(cls, cls.to_yaml)
        self.register_list.append(cls)
        return cls

    def reg_batch(self, *cls_list):
        for cls in cls_list:
            self.register(cls)

    def reg_other(self, yml):
        self.reg_batch(*yml.register_list)

    def data_final(self, data):
        for cls in self.register_list:
            data = cls.data_final(data)
        return data

    def load(self, file, encoding=None, default=DEFAULT_VALUE):
        if not hasattr(file, 'read'):
            if not os.path.isfile(file) and default is not DEFAULT_VALUE:
                return default
            with codecs.open(file, encoding=encoding or self.encoding) as f:
                return self.data_final(pyyaml.load(f, Loader=self.loder))
        else:
            return self.data_final(pyyaml.load(file, Loader=self.loder))

    def loads(self, s):
        if isinstance(s, str):
            s = s.encode(self.encoding)
        return self.load(BytesIO(s))

    def dump(self, file, obj, encoding=None):
        if not hasattr(file, 'write'):
            file = normal_path(file)
            sure_dir(os.path.dirname(file))
            with codecs.open(file, 'w', encoding=encoding or self.encoding) as f:
                return pyyaml.dump(obj, f, Dumper=self.dumper, **self.dump_kwargs)
        else:
            return pyyaml.dump(obj, file, Dumper=self.dumper, **self.dump_kwargs)

    def dumps(self, obj):
        return pyyaml.dump(obj, Dumper=self.dumper, **self.dump_kwargs)


class Resolver:
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    basic = (Loader, Dumper)
    ordereddict = (yamlloader.ordereddict.CLoader, yamlloader.ordereddict.CDumper)

    @staticmethod
    def clone(resolvers):
        loader, dumper = resolvers
        return type('loader', (loader,), dict(
            yaml_constructors=getattr(loader, 'yaml_constructors', {}).copy(),
            yaml_multi_constructors=getattr(loader, 'yaml_multi_constructors', {}).copy(),
        )), type('dumper', (dumper,), dict(
            yaml_representers=getattr(dumper, 'yaml_representers', {}).copy(),
            yaml_multi_representers=getattr(dumper, 'yaml_multi_representers', {}).copy()
        ))


yaml = Yaml(resolvers=Resolver.ordereddict)
yaml.reg_batch(StrTag)
