#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------
import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger('pyagentx2.mib')
logger.addHandler(NullHandler())
# --------------------------------------------


import pyagentx2


class MIB(object):

    def __init__(self):
        self.data = {}
        self.data_idx = []

    def __iter__(self):
        return MibIterator(self)

    def has_oid(self, oid):
        return (oid in self.data)

    def get_oids(self):
        return self.data.keys()

    def delete_oid(self, oid):
        del(self.data[oid])
        self.data_idx = sorted(self.data.keys(), key=lambda k: tuple(int(part) for part in k.split('.')))

    def clear(self):
        self.data = {}
        self.data_idx = []

    def get(self, oid):
        if oid in self.data:
            return self.data[oid]
        else:
            return None

    def get_next(self, oid, endoid):
        next_oid = self._get_next_oid(oid, endoid)
        logger.debug("GET_NEXT: %s => %s" % (oid, next_oid))
        if next_oid is not None:
            value = self.get(next_oid)
            return value
        else:
            return None

    def set(self, oid, type, value):
        self.data[oid] = {'name': oid, 'type': type, 'value': value}
        self.data_idx = sorted(self.data.keys(), key=lambda k: tuple(int(part) for part in k.split('.')))

    ### Helpers
    def set_INTEGER(self, oid, value):
        logger.debug('Setting INTEGER %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_INTEGER, value)

    def set_OCTETSTRING(self, oid, value):
        logger.debug('Setting OCTETSTRING %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_OCTETSTRING, value)

    def set_OBJECTIDENTIFIER(self, oid, value):
        logger.debug('Setting OBJECTIDENTIFIER %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_OBJECTIDENTIFIER, value)

    def set_IPADDRESS(self, oid, value):
        logger.debug('Setting IPADDRESS %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_IPADDRESS, value)

    def set_COUNTER32(self, oid, value):
        logger.debug('Setting COUNTER32 %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_COUNTER32, value)

    def set_GAUGE32(self, oid, value):
        logger.debug('Setting GAUGE32 %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_GAUGE32, value)

    def set_TIMETICKS(self, oid, value):
        logger.debug('Setting TIMETICKS %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_TIMETICKS, value)

    def set_OPAQUE(self, oid, value):
        logger.debug('Setting OPAQUE %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_OPAQUE, value)

    def set_COUNTER64(self, oid, value):
        logger.debug('Setting COUNTER64 %s = %s' % (oid, value))
        self.set(oid, pyagentx2.TYPE_COUNTER64, value)

    def _get_next_oid(self, oid, endoid):
        if oid in self.data:
            # Exact match found
            # logger.debug('get_next_oid, exact match of %s' % oid)
            idx = self.data_idx.index(oid)
            if idx == (len(self.data_idx) - 1):
                # Last Item in MIB, No match!
                return None
            return self.data_idx[idx + 1]
        else:
            # No exact match, find prefix
            # logger.debug('get_next_oid, no exact match of %s' % oid)
            slist = oid.split('.')
            elist = endoid.split('.')
            for tmp_oid in self.data_idx:
                tlist = tmp_oid.split('.')
                for i in range(len(tlist)):
                    try:
                        sok = int(slist[i]) <= int(tlist[i])
                        eok = int(elist[i]) >= int(tlist[i])
                        if not (sok and eok):
                            break
                    except IndexError:
                        pass
                if sok and eok:
                    return tmp_oid
            return None  # No match!


class MibIterator:
    ''' Iterator class '''

    def __init__(self, mib):
        # MIB object reference
        self._mib = mib
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < len(self._mib.data):
            index = self._mib.data.keys()[self._index]
            aux = self._mib.data[index]
            result = (aux['name'], aux['type'], aux['value'])
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration

    def next(self):
        return self.__next__()