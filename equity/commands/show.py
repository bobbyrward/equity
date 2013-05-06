from equity.commands.common import command_registry
from equity.stash import Stash


@command_registry.register(
    name='show',
    description='Show details of a specific patch',
    help_message=None,
    usage='show <patch id or description>',
)
def show_patch_details(args, options, parser):
    if len(args) != 1:
        raise Exception('Must provide the patch id or patch description')

    stash = Stash()

    try:
        patches = stash.find_patches(args[0])
    finally:
        stash.close()

    for patch in patches:
        print patch['id'], patch['date_created'], patch['description']
        print patch['summary']
        print

    return 0

