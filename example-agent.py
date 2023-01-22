#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Rayed Alrashed 2015-06-14

AgentX sub agent that implement some parts of NET-SNMP-EXAMPLES-MIB:
<http://www.net-snmp.org/docs/mibs/NET-SNMP-EXAMPLES-MIB.txt>

snmpwalk -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleScalars
snmptable -v 2c -c public -Ci localhost NET-SNMP-EXAMPLES-MIB::netSnmpIETFWGTable 

Try snmpset:
snmpset -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleInteger.0 i 10
snmpset -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleInteger.0 i 200
snmpset -v 2c -c public localhost NET-SNMP-EXAMPLES-MIB::netSnmpExampleString.0 s "Test"

'''

import random
import pyagentx2


def str_to_oid(data):
    length = len(data)
    oid_int = [str(ord(i)) for i in data]
    return str(length) + '.' + '.'.join(oid_int)


class NetSnmpTestMibScalar(pyagentx2.Updater):

    def update(self, mib):
        # self.set_INTEGER('1.0', 1000)
        # mib.set_OCTETSTRING('1.3.6.1.4.1.8072.2.1.3.0', 'String for NET-SNMP-EXAMPLES-MIB')
        mib.set_OBJECTIDENTIFIER('1.3.6.1.4.1.8072.2.1.4.0', '1.2')
        mib.set_IPADDRESS('1.3.6.1.4.1.8072.2.1.5.0', '127.0.0.1')
        mib.set_COUNTER32('1.3.6.1.4.1.8072.2.1.6.0', 2000)
        mib.set_GAUGE32('1.3.6.1.4.1.8072.2.1.7.0', 2000)
        mib.set_TIMETICKS('1.3.6.1.4.1.8072.2.1.8.0', 1000000)
        mib.set_OPAQUE('1.3.6.1.4.1.8072.2.1.9.0', 'Test')
        mib.set_COUNTER64('1.3.6.1.4.1.8072.2.1.10.0', 2000)


class NetSnmpTestMibTable(pyagentx2.Updater):

    def update(self, mib):
        # implement netSnmpIETFWGTable from NET-SNMP-EXAMPLES-MIB.txt
        # Number of entries in table is random to show that MIB is reset
        # on every update
        for i in range(random.randint(3, 5)):
            idx = str_to_oid('group%s' % (i+1))
            mib.set_OCTETSTRING('1.3.6.1.4.1.8072.2.2.1.1.2.' + idx, 'member 1')
            mib.set_OCTETSTRING('1.3.6.1.4.1.8072.2.2.1.1.3.' + idx, 'member 2')


class NetSnmpIntegerSet(pyagentx2.SetHandler):

    def test(self, oid, type, value, mib):
        if int(value) > 100:
            raise pyagentx2.WrongValueException()

    def commit(self, oid, type, value, mib):
        print("COMMIT CALLED: %s = %s" % (oid, value))
        mib.set(oid, type, value)

class NetSnmpIpSet(pyagentx2.SetHandler):

    def test(self, oid, type, value, mib):
        pass
        # if int(value) > 100:
        #     raise pyagentx2.SetHandlerError()

    def commit(self, oid, type, value, mib):
        print("COMMIT CALLED: %s = %s" % (oid, value))
        mib.set(oid, type, value)

class NetSnmpOctectStringSet(pyagentx2.SetHandler):

    def test(self, oid, type, value, mib):
        pass
        # if int(value) > 100:
        #     raise pyagentx2.SetHandlerError()

    def commit(self, oid, type, value, mib):
        print("COMMIT CALLED: %s = %s" % (oid, value))
        mib.set(oid, type, value)

class MyAgent(pyagentx2.Agent):

    def setup(self):
        self.register('1.3.6.1.4.1.8072.2.1', NetSnmpTestMibScalar)
        self.register('1.3.6.1.4.1.8072.2.2', NetSnmpTestMibTable)
        self.register_set('1.3.6.1.4.1.8072.2.1.1.0', NetSnmpIntegerSet)
        self.register_set('1.3.6.1.4.1.8072.2.1.2.0', NetSnmpIpSet)
        self.register_set('1.3.6.1.4.1.8072.2.1.3.0', NetSnmpOctectStringSet)


def main():
    pyagentx2.setup_logging(debug=False)
    a = MyAgent()
    try:
        a.start()
    except Exception as e:
        print("Unhandled exception:", e)
        a.stop()
    except KeyboardInterrupt:
        a.stop()

if __name__=="__main__":
    main()

