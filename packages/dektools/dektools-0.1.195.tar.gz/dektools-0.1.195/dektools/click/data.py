import json
import typer

app = typer.Typer(add_completion=False)


@app.command(name='format')
def _format(path, fmt, out='', prefix='', ext=''):
    from dynaconf.vendor.dotenv import dotenv_values
    from ..file import read_file, path_ext
    from ..yaml import yaml
    from ..shell import output_data

    ext = ext or path_ext(path)
    if ext == '.env':
        data = dotenv_values(path)
    elif ext == '.json':
        data = json.loads(read_file(path))
    elif ext in ('.yaml', '.yml'):
        data = yaml.loads(read_file(path))
    else:
        raise TypeError(f'Can not read this file format: {path}')
    output_data(data, out, fmt, prefix)
