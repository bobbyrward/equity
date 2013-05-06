from equity.commands.common import command_registry
from equity.stash import Stash
from equity.svn_controller import SvnController


@command_registry.register(
    name='save',
    description='Save the changes in the current checkout as `name`',
    help_message=None,
    usage='save <name>'
)
def save_patch(args, options, parser):
    if len(args) != 1:
        raise Exception('A name for the patch must be provided')

    description = args[0]

    stash = Stash()

    svn = SvnController()

    modified_files = svn.status()
    if not modified_files:
        raise Exception('No changes to stash')

    summary = '\n'.join(' -> '.join(x) for x in modified_files)

    patch = svn.diff()

    try:
        stash.add_patch(patch, summary, description)
    except Exception:
        stash.rollback()
        raise
    else:
        stash.commit()
    finally:
        stash.close()

    return 0

