from importlib import metadata
from .attr import Object


def iter_plugins(name: str, group: str = 'plugins', ignore: set | None = None, **kwargs):
    for ep in metadata.entry_points(group=name.partition('.')[0] + '.' + group, **kwargs):
        if not ignore or ep.name not in ignore:
            yield Object(name=ep.name, module=ep.module, value=ep.load())

# group format: package_name.sub_name
# pdm format:
# [project.entry-points."$group"]
# $ep.name(package_name) = "$ep.module(package_name.module_path):attr_name"
