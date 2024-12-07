import sys
import typer
from ..web.url import Url

app = typer.Typer(add_completion=False)


@app.command()
def auth(url, username, password=None):
    sys.stdout.write(Url.new(url).replace(username=username, password=password).value)
