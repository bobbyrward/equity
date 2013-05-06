import os
import sqlite3
import zlib

from datetime import datetime
from distutils.version import StrictVersion
from hashlib import sha1


VERSION_CREATE_SQL = """
CREATE TABLE version ( version_number TEXT );
"""


STASH_CREATE_SQL = """
CREATE TABLE stash ( id TEXT PRIMARY KEY
                   , date_created TIMESTAMP
                   , deleted BLOB
                   , summary TEXT
                   , description
                   , patch BOOL
                   );
"""


class Stash(object):
    def __init__(self):
        self._load_db()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()

    def _find_storage_dir(self):
        """Return the parent of the .svn directory that the stash will be saved to"""

        cwd = os.getcwd()

        if not os.path.exists('.svn'):
            os.chdir('..')

            if cwd == os.getcwd():
                # at root.  no .svn.
                raise Exception('Unable to find .svn directory')

            return self._find_storage_dir()

        else:
            return cwd

    def _load_db(self):
        storage_dir = self._find_storage_dir()
        db_filename = os.path.join('.svn', 'equity-stash.db')
        need_create_tables = False

        if not os.path.exists(db_filename):
            need_create_tables = True

        self.db = sqlite3.connect(
                db_filename,
                detect_types=sqlite3.PARSE_DECLTYPES,
            )

        self.db.row_factory = sqlite3.Row

        if need_create_tables:
            self._create_tables()

        self._check_version()

    def _create_tables(self):
        import equity

        cursor = self.db.cursor()

        try:
            cursor.execute(VERSION_CREATE_SQL)
            cursor.execute(STASH_CREATE_SQL)
            cursor.execute(
                'INSERT INTO version VALUES (?)',
                (equity.__version__,)
            )
        except Exception:
            pass
        else:
            self.commit()
        finally:
            cursor.close()

    def _check_version(self):
        import equity

        cursor = self.db.cursor()

        try:
            cursor.execute('SELECT * FROM version');

            version = cursor.fetchone()[0]

            if StrictVersion(version) != StrictVersion(equity.__version__):
                self.migrate_versions(version, equity.__version__)

        finally:
            cursor.close()

    def add_patch(self, patch_text, summary, description):
        cursor = self.db.cursor()

        compressed_patch = zlib.compress(patch_text)
        patch_id = sha1(compressed_patch).hexdigest()

        try:
            return cursor.execute(
                u'''
                INSERT INTO stash 
                (id, date_created, deleted, summary, description, patch) 
                VALUES 
                (?, ?, ?, ?, ?, ?)
                ''',
                (
                        patch_id,
                        datetime.now(),
                        False,
                        summary,
                        description,
                        buffer(compressed_patch),
                )
            )
        finally:
            cursor.close()

    def get_all_patches(self):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                'SELECT * FROM stash WHERE deleted=0 ORDER BY date_created DESC'
            )

            return cursor.fetchall()
        finally:
            cursor.close()

    def find_patches(self, filter_arg):
        cursor = self.db.cursor()
        try:
            cursor.execute('''
                SELECT * FROM stash
                    WHERE deleted=0
                    AND   (
                        id = ?
                        OR
                        description LIKE ?
                    )
                ORDER BY date_created DESC
            ''', (filter_arg, ''.join(['%', filter_arg, '%'])))

            return cursor.fetchall()
        finally:
            cursor.close()

    def find_specific_patch(self, filter_arg):
        patches = self.find_patches(filter_arg)

        if len(patches) > 1:
            raise Exception('More than one patch found matching "{}"'.format(
                args[0]
            ))

        if len(patches) == 0:
            raise Exception('No patches found matching "{}"'.format(
                args[0]
            ))

        return patches[0]

