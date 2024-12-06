import sys
import typer
from ..net import is_port_in_use

app = typer.Typer(add_completion=False)


@app.command(name='port')
def port_(port, host='localhost'):
    if is_port_in_use(int(port), host):
        sys.stdout.write('using')
    else:
        sys.stdout.write('free')
