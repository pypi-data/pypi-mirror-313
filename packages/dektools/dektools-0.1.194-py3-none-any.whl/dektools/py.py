import os


def get_whl_name(path):
    return os.path.basename(path).rsplit('-', 4)[0]
