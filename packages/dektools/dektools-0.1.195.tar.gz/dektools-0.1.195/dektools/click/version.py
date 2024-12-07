import sys
import typer
from ..version import version_digits, default_version_sep

app = typer.Typer(add_completion=False)


@app.command()
def digits(version, sep=default_version_sep):
    sys.stdout.write(version_digits(version, sep=sep))
