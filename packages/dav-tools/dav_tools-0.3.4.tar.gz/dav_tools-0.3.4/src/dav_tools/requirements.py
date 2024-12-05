'''Requirements for running a progam.'''

from . import messages as _messages

import os as _os
import ctypes as _ctypes
import platform as _platform
import elevate as _elevate


class OS:
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MAC = 'Mac'


def require(root = False, os: list[str] = []):
    '''
    Require the program to statisfy the given requirements before continuing its execution.

    :param root: If True, the program needs to be run as root (if it isn't already, it automatically tries to relaunch itself with root privileges).
    :param os: Unless the list is empty, the program can be run only on specified OSes. If it isn't, the program terminates.
    '''
    if len(os) > 0:
        _require_os(*os)

    if root:
        _require_root()

def _require_root(auto_elevate=True):
    if auto_elevate:
        _elevate.elevate(graphical=False)

    if _platform.system() == 'Windows':
        if _ctypes.WinDLL('Shell32').IsUserAnAdmin() == 0:
            _messages.critical_error('Program must be run as root')
    else:
        if _os.geteuid() != 0:
            _messages.critical_error('Program must be run as root')

def _require_os(*os: str):
    if _platform.system() not in os:
        _messages.critical_error('OS not supported')


if __name__ == '__main__':
    '''Allow requirements from other programs'''
    from . import argument_parser, ArgumentAction

    argument_parser.set_description('Set script requirements')
    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini95@gmail.com')

    argument_parser.add_argument('--root', action=ArgumentAction.STORE_TRUE, help='script needs to be run with admin privileges')
    argument_parser.add_argument('--os', nargs='+', help='script can only be run on these OSes')

    if argument_parser.args.root:
        _require_root(auto_elevate=False)

    if argument_parser.args.os:
        _require_os(*argument_parser.args.os)

    