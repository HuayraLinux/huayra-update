#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
from datetime import datetime

from gi.repository import PackageKitGlib as packagekit


class APTCache(object):
    USER_HOME = os.path.expanduser('~')
    HU_PATH = os.path.join(USER_HOME, '.huayra-update')
    LAST_SYNC = os.path.join(HU_PATH, 'cache_age')

    def _folder_exists(self):
        if not os.path.exists(self.HU_PATH):
            os.mkdir(self.HU_PATH)

    def mark_last_sync(self):
        self._folder_exists()
        self.last_sync = self.current_time()

        with open(self.LAST_SYNC, 'w') as fp:
            fp.write(str(self.last_sync))

    def get_last_sync(self):
        try:
            with open(self.LAST_SYNC, 'r') as fp:
                self.last_sync = long(fp.read())

        except IOError:
            self.mark_last_sync()

    def current_time(self):
        return long(datetime.now().strftime('%s'))

    def is_old(self):
        self.get_last_sync()

        if (self.current_time() - 86400) > self.last_sync:
            self.mark_last_sync()
            return True

        return False

    def progress_cb(self, status, typ, data=None):
        pass

    def refresh_cache(self):
        client = packagekit.Client()
        client.get_updates(0, None, self.progress_cb, None)

    def available_updates(self):
        task = packagekit.Task()
        packages = task.get_updates(0, None, self.progress_cb, None)
        return len(packages.get_package_array())

    def __init__(self):
        if self.is_old():
            self.refresh_cache()

        if self.available_updates():
            self.updateable = True
        else:
            self.updateable = False


if __name__ == '__main__':
    a = APTCache()
