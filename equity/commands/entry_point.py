import sys
import argparse


from equity.commands.common import command_registry

import equity.commands.apply
import equity.commands.clear
import equity.commands.drop
import equity.commands.help
import equity.commands.list
import equity.commands.pop
import equity.commands.save


def execute_command(command, args, options, parser):
    try:
        command_func = command_registry.get_command_entry_point(command)
    except KeyError:
        print 'Unknown command {}'.format(command)
        return 1

    return command_func(args, options, parser)


def main():
    parser = argparse.ArgumentParser(description='An svn change stash')

    parser.add_argument('command', action='store', default='help',
            nargs='?', metavar='COMMAND')
    parser.add_argument('args', nargs=argparse.REMAINDER)

    parsed_arguments = parser.parse_args()

    if parsed_arguments.command is None:
        parsed_arguments.command = 'help'

    return execute_command(
            parsed_arguments.command,
            parsed_arguments.args,
            parsed_arguments,
            parser,
        )
