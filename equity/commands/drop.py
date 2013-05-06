from equity.commands.common import command_registry
from equity.stash import Stash

#TODO: Should have a flag to _really_ delete a patch


@command_registry.register(
    name='drop',
    description='Archive the specified patch',
    help_message=None,
    usage='drop <patch id or name>',
)
def drop_patch(args, options, parser):
    if len(args) != 1:
        raise Exception('Must provide the patch id or patch description')

    stash = Stash()

    try:
        patch = stash.find_specific_patch(args[0])
        stash.archive_patch(patch['id'])
    except Exception:
        stash.rollback()
        raise
    else:
        stash.commit()
        print 'Archived patch {}.'.format(patch['id'])
    finally:
        stash.close()

    return 0

