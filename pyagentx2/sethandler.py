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


class GenErrException(Exception):
    pass

class NoAccessException(Exception):
    pass

class WrongTypeException(Exception):
    pass

class WrongLengthException(Exception):
    pass

class WrongEncodingException(Exception):
    pass

class WrongValue(Exception):
    pass

class NoCreation(Exception):
    pass

class InconsistentValue(Exception):
    pass

class ResourceUnavailable(Exception):
    pass

class NotWritable(Exception):
    pass

class InconsistentName(Exception):
    pass


class SetHandler(object):

    # User override these 
    def test(self, oid, type, value, mib):
        pass

    def commit(self, oid, type, value, mib):
        pass

