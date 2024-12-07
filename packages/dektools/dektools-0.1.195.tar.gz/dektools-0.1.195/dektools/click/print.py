import os
import json
import typer
from typing import Annotated, Optional
from configparser import ConfigParser

app = typer.Typer(add_completion=False)

typed_map = {'json': {'.json'}, 'yaml': {'.yaml', '.yml'}, 'cfg': {'.ini', '.cfg'}}
typed_map_reversed = {ext: t for t, s in typed_map.items() for ext in s}


@app.command()
def data(filepath,
         expression: Annotated[str, typer.Argument()] = '',
         typed: Annotated[Optional[str], typer.Option('--type')] = ''):
    from ..yaml import yaml
    from ..file import read_text
    from ..output import print_data_or_value

    if not typed:
        ext = os.path.splitext(filepath)[-1].lower()
        typed = typed_map_reversed[ext]
    if typed == 'json':
        d = json.loads(read_text(filepath))
    elif typed == 'yaml':
        d = yaml.load(filepath)
    elif typed == 'cfg':
        parser = ConfigParser()
        parser.read(filepath)
        d = {section: dict(parser.items(section)) for section in parser.sections()}
    else:
        raise TypeError(f"Invalid type: {typed}")
    print_data_or_value(d, expression)
