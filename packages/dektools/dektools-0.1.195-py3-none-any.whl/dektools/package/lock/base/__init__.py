import sys
from ....shell import shell_exitcode


def try_lock(name, path):
    command = f"dekpkglock lock {name} {path}"
    exitcode = shell_exitcode(command)
    if exitcode:
        sys.stdout.write(f"Warning: No lock file, you can see details by running: `{command}`\n")
