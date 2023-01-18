#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------
import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pyagentx2.sethandler')
logger.addHandler(NullHandler())
# --------------------------------------------

class SetHandlerError(Exception):
    pass

class SetHandler(object):

    # User override these 
    def test(self, oid, type, value, mib):
        pass

    def commit(self, oid, type, value, mib):
        pass

