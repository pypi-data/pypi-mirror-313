import os
import shelve
from typing import List, Tuple

from .base_backend import BaseExceptionStore
from filelock import Timeout, FileLock

from datetime import datetime


class ShelveStore(BaseExceptionStore):
    """
    ShelveStore uses a bunch of files and python datastructures,
    to store necessary exception data
    should generally be used in low volume environment and tests.
    """

    SHELVE_FILE = 'tiny-turret.db'
    LOCK_FILE = 'tiny-turret.db.lock'
    LOCK_FILE_TIMEOUT_S = 3

    def __init__(self, settings):
        super().__init__(settings)
        self._db = None

    @property
    def db(self):
        if self._db is None:

            self.lock_path = os.path.join(self.settings['path'], self.LOCK_FILE)
            self.path = os.path.join(self.settings['path'], self.SHELVE_FILE)

            self.lock = FileLock(self.lock_path, timeout=self.LOCK_FILE_TIMEOUT_S)
            self.lock.acquire()
            self._db = shelve.open(self.path)
        return self._db

    def __del__(self):
        if self._db:
            self._db.close()
        if self.lock:
            self.lock.release()

    def clear_db(self):
        self.db.clear()

    def append_group_list(self, group_key, error_count, key_exists):
        # <group_key, error_count>
        # highest error count at the beginning of the list.
        group_list = self.db.get('group_list', [])

        if not key_exists:
            group_list.append(
                (group_key, error_count)
            )
        else:
            for idx, val in enumerate(group_list):
                if val[0] == group_key:
                    group_list[idx] = (group_key, error_count)
        group_list.sort(key= lambda x: x[1], reverse=True)
        if len(group_list) > self.MAX_EXCEPTION_GROUPS:
            group_list.pop()
        self.db['group_list'] = group_list

    def save_group(self, group_key, group_struct):
        key_exists = group_key in self.db
        db_group_struct = self.db[group_key].copy() if key_exists else group_struct

        if 'first_seen' not in db_group_struct:
            db_group_struct['first_seen'] = datetime.now().isoformat()

        # increment error count
        db_group_struct['error_count'] += 1
        db_group_struct['last_seen'] = datetime.now().isoformat()

        self.append_group_list(group_key, db_group_struct['error_count'], key_exists)

        # save
        self.db[group_key] = db_group_struct

    def get_exc_list(self, group_key):
        exc_key = 'exceptions_list:' + group_key
        exc_list = self.db.get(exc_key, [])
        return exc_list

    def save_exception(self, group_key, group_struct, exc_struct):
        # TODO: trim lists.

        self.save_group(group_key, group_struct)

        exc_list = self.get_exc_list(group_key)
        exc_key = 'exceptions_list:' + group_key
        exc_list.insert(0, exc_struct)
        if len(exc_list) >= self.MAX_EXCEPTIONS_PER_GROUP:
            exc_list.pop()
        self.db[exc_key] = exc_list

    def get_group_list(self, limit=10):
        group_list: List[Tuple[str, int]] = self.db.get('group_list', [])
        return [
            {
                'group_key': group_key,
                'info':self.db.get(group_key)
            } for group_key, _ in group_list[:limit]
        ]

    def get_exceptions(self, group_key, limit=10):
        exc_list = self.get_exc_list(group_key)[:limit]
        return exc_list
