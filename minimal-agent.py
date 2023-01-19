#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyagentx2

# Updater class that set OID values
class NetSnmpPlaypen(pyagentx2.Updater):
    def update(self, mib):
        mib.set_INTEGER('1.0', 1000)
        mib.set_OCTETSTRING('3.0', 'String for NET-SNMP-EXAMPLES-MIB')


class MyAgent(pyagentx2.Agent):
    def setup(self):
        # Register Updater class that responsd to
        # the tree under "netSnmpPlaypen": 1.3.6.1.4.1.8072.9999.9999
        self.register('1.3.6.1.4.1.8072.9999.9999', NetSnmpPlaypen)


# Main 
pyagentx2.setup_logging()
a = MyAgent()
try:
    a.start()
except Exception as e:
    print "Unhandled exception:", e
    a.stop()
except KeyboardInterrupt:
    a.stop()
