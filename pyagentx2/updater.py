#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------
import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pyagentx2.updater')
logger.addHandler(NullHandler())
# --------------------------------------------

import time
import threading


class Updater(threading.Thread):

    def __init__(self, mib, oid, freq):
        threading.Thread.__init__(self)
        self.stop = threading.Event()

        self.mib = mib
        self._oid = oid
        self._freq = freq



    def run(self):
        start_time = 0
        while True:
            if self.stop.is_set(): break
            now = time.time()
            if now - start_time > self._freq:
                logger.info('Updating : %s (%s)' % (self.__class__.__name__, self._oid))
                start_time = now
                self.update(self.mib)
            time.sleep(0.1)
        logger.info('Updater stopping')

    # Override this
    def update(self, mib):
        pass
