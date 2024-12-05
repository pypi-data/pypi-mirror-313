'''Customized argument parser.'''

import argparse
from . import text_format

class ArgumentAction:
    STORE = 'store'
    STORE_CONST = 'store_const'
    STORE_TRUE = 'store_true'
    STORE_FALSE = 'store_false'
    APPEND = 'append'
    APPEND_CONST = 'append_const'
    COUNT = 'count'
    EXTEND = 'extend'
    BOOLEAN_OPTIONAL = argparse.BooleanOptionalAction


class ArgumentParser:
    '''
    Customized argument parser.

    Options and/or flags can be easily added, optionally inside (exclusive) groups.
    Some flags are automatically set.

    Command line options are parsed when calling for the first time the `args` property.
    '''

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )

        self.__groups = {}


    def set_version(self, version: str):
        '''
        Add a ``--version`` option, which automatically displays project version.
        
        :param version: Current project version to display.
        '''

        self.parser.add_argument('--version', action='version', version=f'%(prog)s {version}')

    def set_description(self, description: str):
        '''
        Set a brief description of the program, to be displayed on top when using the --help flag.

        :param description: A description of the program
        '''

        self.parser.description = description

    def set_developer_info(self, name: str, email: str):
        '''
        Set information about the developer of the project.
        These informations will be displayed at the bottom of the --help command. 

        :param name: Name to be displayed
        :param email: Email address to be displayed
        '''

        self.parser.epilog = text_format.format_text(f'--Developed by {name} ({email})', text_format.TextFormat.Style.ITALIC)

    @property
    def args(self) -> argparse.Namespace:
        '''
        Parse and return arguments specified on command line.

        :returns: The arguments
        '''
        return self.parser.parse_args()
    

    def __group(self, name: str, description: str = None) -> argparse._ArgumentGroup:
        '''
        Return an argument group, or create it if it doesn't exist.

        :param name: Name of the group
        :param description: Group description

        :returns: The argument group
        '''

        if name in self.__groups:
            return self.__groups[name] 

        if description is None:
            group = self.parser.add_argument_group(name)
        else:
            group = self.parser.add_argument_group(name, text_format.format_text(description, text_format.TextFormat.Style.ITALIC))

        self.__groups[name] = group
        return group

    def add_mutually_exclusive_group(self, parent: argparse._ArgumentGroup = None) -> argparse._MutuallyExclusiveGroup:
        '''
        Create a mutually exclusive argument group.
        Only one option from this group can be used at a time.

        :param parent: If specified, create the new group as subgroup of parent, otherwise create it at top level

        :returns: The new mutually exclusive group
        '''
        
        if parent is None:
            parent = self.parser

        return parent.add_mutually_exclusive_group()

    def add_argument(self,
                     *name_or_flags,
                     group: argparse.ArgumentParser | argparse._ArgumentGroup | argparse._MutuallyExclusiveGroup | str = None,
                     **kwargs):
        '''
        Add an argument to the parser.

        :param name_or_flags: Name or flags of the new argument. These options are directly passed to the argparse library.
        :param group: Group in which to create the new argument. Can also be specified in string format.
        :param kwargs: Additional options to be passed to the underlying argparse library.
        '''
        
        if group is None:
            group = self.parser
        elif type(group) == str:
            group = self.__group(group)

        group.add_argument(*name_or_flags, **kwargs)

    def add_quiet_mode(self):
        '''
        Add a ``--quiet`` switch, which can be used in the program to suppress some output.
        Group and description are automatically set.
        '''
        
        self.add_argument('--quiet', group=self.__group('verbosity'), help='Suppresses all non-critical messages', action=ArgumentAction.STORE_TRUE)

    def add_verbose_mode(self):
        '''
        Add a ``--verbose`` switch, which can be used in the program to produce more output.
        Group and description are automatically set.
        '''
        
        self.add_argument('--verbose', group=self.__group('verbosity'), help='Prints additional debug messages', action=ArgumentAction.STORE_TRUE)

    @property
    def is_verbose(self):
        return 'verbose' in self.args and self.args.verbose


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.set_description('This module provides an easy-to-use way to handle command line arguments')
    argparser.set_version('1.0')

    argparser.add_argument('input_file', group='files', help='first input file', nargs='?')
    argparser.add_argument('input_file_2', group='files', help='second input file', nargs='*')
    argparser.add_argument('-o', '--output', group='files', help='output files', nargs='+')
    
    argparser.add_quiet_mode()
    argparser.add_verbose_mode()

    print(argparser.args)
