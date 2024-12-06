import os
import tempfile
import zipfile
import shutil
from io import BytesIO
from .file import remove_path, sure_dir, sure_read, normal_path


def compress_files(
        src, path_zip=None, path_set=None, combine=False,
        compression=zipfile.ZIP_BZIP2,
        allowZip64=True,
        compresslevel=9,
        **kwargs):
    src = normal_path(src)
    if path_zip is None:
        zip_file = BytesIO()
    else:
        path_zip = normal_path(path_zip)
        sure_dir(os.path.dirname(path_zip))
        if not combine:
            remove_path(path_zip)
        zip_file = path_zip
    with zipfile.ZipFile(
            zip_file, mode='w',
            compression=compression,
            allowZip64=allowZip64,
            compresslevel=compresslevel,
            **kwargs
    ) as zf:
        if path_set is None:
            for base, _, files in os.walk(src):
                for file in files:
                    p = os.path.join(base, file)
                    zf.write(
                        p,
                        p[len(src):]
                    )
        else:
            for p in path_set:
                p = normal_path(p)
                if not p.startswith(src + os.path.sep):
                    raise ValueError(f'[{p}] not child of [{src}]')
                zf.write(
                    p,
                    p[len(src):]
                )
    return zip_file.getvalue() if path_zip is None else zip_file


def decompress_files(zip_file, dest_dir=None, combine=False):
    if not dest_dir:
        dest_dir = tempfile.mkdtemp()
    dest_dir = os.path.normpath(os.path.abspath(dest_dir))
    if not combine:
        remove_path(dest_dir)
    sure_dir(dest_dir)
    try:
        with zipfile.ZipFile(sure_read(zip_file)) as zip_ref:
            zip_ref.extractall(dest_dir)
    except zipfile.BadZipfile:
        shutil.unpack_archive(zip_file, dest_dir)
    return dest_dir


def take_bytes(zip_file, path_in_zip):  # path_in_zip is a relative path in zip file
    with zipfile.ZipFile(sure_read(zip_file)) as zip_ref:
        try:
            return zip_ref.read(path_in_zip)
        except KeyError:
            return None


def take_file(zip_file, path_in_zip, path_out):
    sure_dir(os.path.dirname(path_out))
    with zipfile.ZipFile(sure_read(zip_file)) as zip_ref:
        try:
            with zip_ref.open(path_in_zip) as zf, open(path_out, 'wb') as f:
                shutil.copyfileobj(zf, f)
            return True
        except KeyError:
            return False
