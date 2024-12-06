import os
import glob
import typer
from typing import Optional, List
from typing_extensions import Annotated
from ..typer import command_mixin

app = typer.Typer(add_completion=False)


@app.command()
def remove(path, ignore='.rmignore'):
    from ..file import normal_path, remove_path, FileHitChecker

    def walk(fp, is_hit, _):
        if not is_hit:
            remove_path(fp)

    path = normal_path(path)
    if os.path.isdir(path):
        FileHitChecker(path, ignore).walk(walk)
    elif os.path.isfile(path):
        if not FileHitChecker(os.path.dirname(path), ignore).is_hit(path):
            remove_path(path)


@app.command()
def merge(dest, src, ignore=None):
    from ..file import merge_assign, FileHitChecker

    if ignore:
        FileHitChecker(src, ignore).merge_dir(dest)
    else:
        merge_assign(dest, src)


@app.command()
def remove(filepath):
    from ..file import remove_path

    remove_path(filepath)


@app.command()
def write(
        filepath,
        s=None, b=None, sb=None,
        m=None, mi=None,
        c=None, ci=None,
        ma=None, mo=None, mie=None,
        t: Annotated[bool, typer.Option("--t/--no-t")] = False,
        encoding='utf-8'):
    from ..file import write_file

    write_file(
        filepath,
        s=s, b=b, sb=sb,
        m=m, mi=mi,
        c=c, ci=ci,
        ma=ma, mo=mo, mie=mie,
        t=t,
        encoding=encoding
    )


@command_mixin(app, name='glob')
def glob_(args, path):
    from ..shell import shell_wrapper
    result = glob.glob(path, recursive=True)
    if result:
        shell_wrapper(args.format(filepath=result[-1]))


@command_mixin(app)
def globs(args, path):
    from ..shell import shell_wrapper
    result = glob.glob(path, recursive=True)
    for file in result:
        shell_wrapper(args.format(filepath=file))


@app.command()
def compress(src, dest):
    from ..zip import compress_files
    compress_files(src, dest)


@app.command()
def decompress(src, dest, combine: Annotated[bool, typer.Option("--combine/--no-combine")] = False):
    from ..zip import decompress_files
    decompress_files(src, dest, combine)


@app.command()
def backup(src, dest, ignore: Annotated[Optional[List[str]], typer.Option()] = None):
    from ..file import remove_path, copy_recurse_ignore
    from ..zip import compress_files
    path_out = copy_recurse_ignore(src, ignores=['.gitignore', *ignore])
    compress_files(path_out, dest)
    remove_path(path_out)
