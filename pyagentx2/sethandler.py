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

class WrongValueException(Exception):
    pass

class NoCreationException(Exception):
    pass

class InconsistentValueException(Exception):
    pass

class ResourceUnavailableException(Exception):
    pass

class NotWritableException(Exception):
    pass

class InconsistentNameException(Exception):
    pass

class CommitFailedException(Exception):
    pass


class SetHandler(object):

    # User override these 
    def test(self, oid, type, value, mib):
        pass

    def commit(self, oid, type, value, mib):
        pass

