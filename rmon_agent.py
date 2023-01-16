#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

snmpwalk -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleScalars
snmptable -v 2c -c public -Ci localhost NET-SNMP-EXAMPLES-MIB::netSnmpIETFWGTable

Try snmpset:
snmpset -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleInteger.0 i 10
snmpset -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleInteger.0 i 200
snmpset -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleString.0 s "Test"

'''

import time
import random
import pyagentx2
import logging



class FilterTableUpdater(pyagentx2.Updater):

    def update(self):
        # implement netSnmpIETFWGTable from NET-SNMP-EXAMPLES-MIB.txt
        # Number of entries in table is random to show that MIB is reset
        # on every update
        pass
        #self.set_INTEGER('1.1.11.50', 0)

class FilterTableSetHandler(pyagentx2.SetHandler):

    def test(self, oid, data):
        logging.info(data)
        pass
        # if int(data) > 100:
        #     raise pyagentx2.SetHandlerError()

    def commit(self, oid, data):
        print "COMMIT CALLED: %s = %s" % (oid, data)

class MyAgent(pyagentx2.Agent):

    def setup(self):

        self.register('1.3.6.1.2.1.16.7', FilterTableUpdater)
        self.register_set('1.3.6.1.2.1.16.7', FilterTableSetHandler)



def main():
    pyagentx2.setup_logging(debug=True)
    # try:
    a = MyAgent()
    a.start()
    # except Exception as e:
    #     print "Unhandled exception:", e
    #     a.stop()
    # except KeyboardInterrupt:
    #     a.stop()

if __name__=="__main__":
    main()

