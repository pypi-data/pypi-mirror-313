'''Utilities useful during development'''

import importlib as _importlib
from types import ModuleType as _ModuleType
import sys as _sys
import os as _os

def reload_module(module: _ModuleType):
    '''
    Hot-reload an imported module

    :param module: The module to reload
    '''

    _importlib.reload(module)

def import_from(folder: str, module: str):
    '''
    Import a module from any folder
    
    :param folder: Path to the folder containing the module. Can be either absolute or relative.
    :param module: Name of the module to import.
    '''
    
    try:
        path = _os.path.abspath(folder)
        _sys.path.insert(1, path)

        _importlib.import_module(module)
    finally:
        _sys.path.remove(path)