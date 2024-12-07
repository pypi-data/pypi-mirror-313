import typing
from pathlib import Path

import yaml
# from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


#
# YAML Functions
#


def str_presenter(dumper, data):
    text_list = [line.rstrip() for line in data.splitlines()]
    fixed_data = "\n".join(text_list)
    if len(text_list) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", fixed_data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", fixed_data)


Dumper.add_representer(str, str_presenter)

Dumper.ignore_aliases = lambda *args: True
yaml.representer.SafeRepresenter.add_representer(
    str, str_presenter
)  # to use with safe_dum


def yaml_load(path) -> typing.Any:
    with open(path, "r") as f:
        return yaml.load(f, Loader=Loader)


def yaml_dumps(data: typing.Any, sort_keys: bool = False, **kwargs) -> str:
    return yaml.dump(data, Dumper=Dumper, sort_keys=sort_keys, **kwargs)


def yaml_loads(data: str) -> typing.Any:
    return yaml.load(data, Loader=Loader)


def yaml_dump(path: str | Path, data: typing.Any, sort_keys=False, **kwargs) -> None:
    with open(path, "w") as f:
        return yaml.dump(data, f, Dumper=Dumper, sort_keys=sort_keys, **kwargs)
