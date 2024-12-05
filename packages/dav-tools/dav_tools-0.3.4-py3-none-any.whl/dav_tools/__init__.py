'''Python library to aid in software development.'''

# ARGUMENT PARSER
#   Hides package and only shows one instance of the class
from . import _arg_parser as _arg_parser
from ._arg_parser import ArgumentAction

argument_parser = _arg_parser.ArgumentParser()
'''Argument parser instance -- use this instead of importing the ``_arg_parser`` module.'''

# ...