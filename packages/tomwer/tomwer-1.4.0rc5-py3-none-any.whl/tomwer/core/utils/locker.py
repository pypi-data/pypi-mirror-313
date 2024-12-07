# coding: utf-8
from __future__ import annotations

import os
from flufl.lock import Lock

from tomwer.core.utils.Singleton import singleton

_FILE_LOCKERS = {}


def get_lock_file_path(process_file_path):
    process_file_path = os.path.abspath(process_file_path)
    parts = process_file_path.split(os.sep)
    if len(parts) == 0:
        # file without any name ???!!!
        raise RuntimeError
    elif len(parts) == 1:
        file_path = ""
    else:
        file_path = os.path.join(*parts[:-1])
    lock_name = "." + parts[-1] + ".flufllock"
    return os.path.join(file_path, lock_name)


@singleton
class FileLockerManager:
    """Insure that for each file we will provide at most one locker"""

    def __init__(self):
        self.__lockers = {}

    def clear_locker(self, file_):
        if file_ in self.__lockers:
            del self.__lockers[file_]

    @staticmethod
    def get_lock(file_name):
        def get_lock_file_path(file_path):
            file_path = os.path.abspath(file_path)
            parts = file_path.split(os.sep)
            if len(parts) == 0:
                # file without any name ???!!!
                raise RuntimeError
            elif len(parts) == 1:
                file_path = ""
            else:
                file_path = os.sep.join(parts[:-1])
            lock_name = "." + parts[-1] + ".flufllock"
            return os.path.join(file_path, lock_name)

        lock_file_path = get_lock_file_path(file_name)
        # if not os.path.exists(lock_file_path):
        #     from pathlib import Path
        #     Path(lock_file_path).touch()
        if lock_file_path not in _FILE_LOCKERS:
            _FILE_LOCKERS[lock_file_path] = Lock(lock_file_path, default_timeout=3)
        return _FILE_LOCKERS[lock_file_path]
