'''File operations.'''

import shutil as _shutil
from pathlib import Path as _Path


def copy_file(src_path: str, dest_path: str, *, symlink: bool = False):
    '''
        Copy a file from the source path to the destination path, with an option to create a symlink.

        :param src_path: the path of the source file to be copied
        :param dest_path: the path where the file should be copied
        :param symlink: if `True`, a symlink is created at the destination instead of copying the file (default is `False`)

        :raises Exception: if the source path is not a valid file

        :returns: None
    '''
    
    src = _Path(src_path)
    dest = _Path(dest_path)

    if not src.is_file():
        raise Exception(f'{src} is not a file')

    if dest.exists():
        dest.unlink()

    if symlink:
        dest.symlink_to(src)
    else:
        _shutil.copyfile(src, dest)