import os.path
import sys

from equity.commands.common import command_registry


USAGE = """usage: {exec_name} [COMMAND] ...

An svn patch stash

commands:
{commands_text}
"""


def global_help():
    commands_text = []

    for command in sorted(command_registry.registry.keys()):
        commands_text.append((
            '    ',
            command,
            '\t\t',
            command_registry.registry[command]['description']
        ))

    print USAGE.format(
            exec_name=os.path.basename(sys.argv[0]),
            commands_text='\n'.join(''.join(x) for x in commands_text),
        )



def command_help(command):
    pass


@command_registry.register(
    name='help',
    description='Show a list of available commands',
    help_message=None,
)
def entry_point(args, options, parser):
    if not args or args[0] == 'help':
        global_help()
    else:
        command_help(args[0])

    return 0
