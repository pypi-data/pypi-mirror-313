import hashlib
from .file import sure_read

algorithms = hashlib.algorithms_guaranteed


def hash_file(algorithm, path, block_size=64 * 2 ** 10, args=None):  # algorithm: hashlib.__always_supported
    def update(f):
        for chunk in iter(lambda: f.read(block_size), b""):
            hs.update(chunk)

    hs = getattr(hashlib, algorithm)()
    file = sure_read(path)
    if hasattr(file, 'read'):
        update(file)
    else:
        with open(file, "rb") as file:
            update(file)
    return hs.hexdigest(*(args or ()))
