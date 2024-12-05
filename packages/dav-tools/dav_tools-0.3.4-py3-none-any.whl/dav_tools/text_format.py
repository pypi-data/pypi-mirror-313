'''Utilities for handling text formatting.'''

import sys as _sys
import os as _os
from ._text_format import TextFormat


def _get_format(*options) -> str:
    '''
    Get the format string generated from the arguments.
    Needed for manually setting text style. Otherwise use ``set_format()``.

    :param option: Text styling options.

    :returns: The format string corresponding to the options.
    '''

    result = ''

    for option in options:
        if option is not None:
            result += option.decode()

    return result

def _set_format(*options, file = _sys.stdout):
    '''
    Set text styling.

    :param option: Text styling options.
    :param file: Where to set text styling.
    '''

    for option in options:
        if option is not None:
            print(option.decode(), end='', file=file)

def format_text(text: str, *format_options) -> str:
    '''
    Return a styled text.

    :param text: Text to print.
    :param format_options: Text styling options.

    :returns: The text properly styled.
    '''
    
    result = ''
    result += _get_format(*format_options)
    result += text
    result += _get_format(TextFormat.RESET)

    return result

def print_text(text: str = '', *format_options, end: str='\n', file=_sys.stdout, flush=False):
    '''
    Print a styled text.

    :param text: Text to print.
    :param format_options: Text styling options.
    :param end: Character to be printed after the text.
    :param file: Where to print the text.
    :param flush: Whether to flush the stream after printing.
    '''

    text = format_text(text, *format_options)
    print(text, end=end, file=file, flush=flush)

def input_formatted(*format_options) -> str:
    '''
    Ask input from a user using specified styling options.

    :param format_options: Text styling options.

    :returns: User input.
    '''

    result = None

    try:
        _set_format(*format_options, file=_sys.stderr)
        result = input()
        _set_format(TextFormat.RESET, file=_sys.stderr)
    except KeyboardInterrupt as e:
        _set_format(TextFormat.RESET, file=_sys.stderr)
        raise e

    return result

def clear_line(file=_sys.stdout, flush=False):
    '''
    Clears the current line from any text of formatting.
    Not really suitable for files.

    :param file: Stream to clear.
    :param flush: Whether to flush the stream after printing.
    '''
    
    try:
        size = _os.get_terminal_size().columns
        print('\r', ' ' * size, '\r',
              sep='', end='', file=file, flush=flush)
    except OSError:
        pass    # Do nothing

    