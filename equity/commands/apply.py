import zlib

from equity.commands.common import command_registry
from equity.stash import Stash
from equity.patch import apply_patch


@command_registry.register(
    name='apply',
    description='Apply the specified changes to the current checkout',
    help_message=None,
    usage='apply <patch id or name>',
)
def save_patch(args, options, parser):
    if len(args) != 1:
        raise Exception('Must provide the patch id or patch description')

    stash = Stash()

    try:
        patch = stash.find_specific_patch(args[0])['patch']

        apply_patch(zlib.decompress(patch))

        # flag the patch as deleted?

    finally:
        stash.close()

    return 0
