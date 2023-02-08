#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------
import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pyagentx2.agent')
logger.addHandler(NullHandler())
# --------------------------------------------

import time
import inspect

import pyagentx2
from pyagentx2.updater import Updater
from pyagentx2.network import Network
from pyagentx2.mib import MIB



class AgentError(Exception):
    pass

class Agent(object):

    def __init__(self):
        self._oid_list = []
        self._updater_list = []
        self._sethandlers = {}
        self._threads = []
        self.mib = MIB()

    def register(self, oid):
        # cleanup and test oid
        try:
            oid = oid.strip(' .')
            [int(i) for i in oid.split('.')]
        except ValueError:
            raise AgentError('OID isn\'t valid')
        self._oid_list.append(oid)

    def register_updater(self, oid, class_, freq=10):
        if Updater not in inspect.getmro(class_):
            raise AgentError('Class given isn\'t an updater')
        # cleanup and test oid
        try:
            oid = oid.strip(' .')
            [int(i) for i in oid.split('.')]
        except ValueError:
            raise AgentError('OID isn\'t valid')
        self._updater_list.append({'oid':oid, 'class':class_, 'freq':freq})

    def register_set(self, oid, class_, *args, **kwargs):
        if pyagentx2.SetHandler not in inspect.getmro(class_):
            raise AgentError('Class given isn\'t a SetHandler')
        # cleanup and test oid
        try:
            oid = oid.strip(' .')
            [int(i) for i in oid.split('.')]
        except ValueError:
            raise AgentError('OID isn\'t valid')
        self._sethandlers[oid] = class_(*args, **kwargs)


    def start(self):

        # Start Updaters
        for u in self._updater_list:
            logger.debug('Starting updater [%s]' % u['oid'])
            t = u['class'](self.mib, u['oid'], u['freq'])
            t.start()
            self._threads.append(t)

        # Start Network
        t = Network(self.mib, self._oid_list, self._sethandlers)
        t.start()
        self._threads.append(t)

        # Do nothing ... just wait for someone to stop you
        while True:
            #logger.debug('Agent Sleeping ...')
            time.sleep(1)

    def stop(self):
        logger.debug('Stop threads')
        for t in self._threads:
            t.stop.set()
        logger.debug('Wait for updater')
        for t in self._threads:
            t.join()

