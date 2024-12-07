import typer
from typing import Annotated, Optional
from ..typer import command_mixin, annotation

app = typer.Typer(add_completion=False)


@command_mixin(app)
def retry(args, retry_times: Annotated[Optional[int], annotation.Option('--times')] = -1):
    from ..shell import shell_retry

    shell_retry(args, retry_times if retry_times >= 0 else None)


@command_mixin(app)
def headless(args, sync: Annotated[bool, annotation.Option("--sync/--no-sync")] = True):
    from ..shell import shell_command_nt_headless

    shell_command_nt_headless(args, sync)


@command_mixin(app)
def admin(args):
    from ..shell import shell_command_nt_as_admin

    shell_command_nt_as_admin(args)
