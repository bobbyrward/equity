from equity.commands.common import command_registry
from equity.stash import Stash

#TODO: Add a flag to list archived patches
#TODO: Maybe see if we can emulated git and invoke a pager if it fills the screen?


@command_registry.register(
    name='list',
    description='List available patches for this checkout',
    help_message=None,
    usage='list'
)
def list_patches(args, options, parser):
    stash = Stash()

    try:
        patches = stash.get_all_patches()
    finally:
        stash.close()

    for patch in patches:
        print patch['id'], patch['date_created'], patch['description']

    return 0
