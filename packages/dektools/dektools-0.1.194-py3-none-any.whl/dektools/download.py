import os
from urllib.parse import urlparse
from .file import sure_dir, remove_path
from .shell import shell_wrapper, shell_exitcode


def download_http_auth(username=None, password=None):
    auth = ''
    if username:
        auth += f' -u {username}'
        if password:
            auth += f':{password}'
    return auth


def download_http_exist(url, username=None, password=None):
    return shell_exitcode(
        f"curl --output /dev/null --silent --head --fail {url}{download_http_auth(username, password)}"
    ) == 0


def download_from_http(url, path_dest, username=None, password=None):
    sure_dir(os.path.dirname(path_dest))
    remove_path(path_dest)
    shell_wrapper(f'curl -fLSs {url} -o {path_dest}{download_http_auth(username, password)}')


def download_from_git(url, path_dest):
    sure_dir(path_dest)
    ul = url.split('+', 1)
    b = []
    if len(ul) > 1:
        b = ['-b', ul[1]]
    sub = ' '.join([*b, ul[0]])
    shell_wrapper(f'git clone  {sub} .')


def download_tree_from_http(path_dest, url_list, username=None, password=None):
    result = {}
    for url in url_list:
        pr = urlparse(url)
        path = pr.path[1:]
        result[url] = path
        filepath = os.path.join(path_dest, path)
        download_from_http(url, filepath, username, password)
    return result
