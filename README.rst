.. EQUITY

equity
================================================================================

A stash for svn patches


Rationale
--------------------------------------------------------------------------------

I've not been able to find a good replacement for 'git stash' when working with 
svn.  Our current workflow requires a code review before commit.  This causes
some issues when working on multiple changes at the same time.

Some issues this tools seeks to improve upon over other implementations:


Atomicity
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
If a problem arises applying the patch or saving the patch, don't entirely lose
all of the changes.  Do absolutely nothing.  I've lost patches because of issues
writing out the patch file locally because the changes were reverted beforehand.


Archiving
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Keep an archive of all patches and don't actually delete them except when
explicitly told to through maintenance commands.  Patches are instead marked as
deleted and kept in the datastore.


Storage Backend
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Use sqlite as the storage backend for better querying.  Store changes in the
root .svn directory of the checkout.


Easily installable
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
The tool should be easily installable with pip and provide entry points through
the standard method of distribute


Safe defaults
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Don't make the default command store the current patch


Better logging
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Log everything of interest


Warnings as errors
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Be much more careful of issues.  If a potential issue is seen, don't assume
that's ok.  Error out and let the user handle it, possibly by specifiying a flag
to be unsafe.
