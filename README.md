
# Python AgentX Implementation

"pyagentx2" is a fork of [pyagentx](https://github.com/hosthvo/pyagentx), which is a pure Python implementation of AgentX protocol ([RFC 2741](http://www.ietf.org/rfc/rfc2741.txt)), that
allows you to extend SNMP agent (snmpd) by writing AgentX subagents, without modifying your original SNMP agent.

This version counts with some modifications from the original pyagentx to fit my own purposes. If you don't need any of the characteristics listed in the [change log](#change-log) section I recomend you to use the original [pyagentx](https://github.com/hosthvo/pyagentx).


## Features

Currently, the code is capable of the following:

* Open a session with AgentX master, e.g. net-snmpd snmpd, and register a new session.
* Send Ping request.
* Register multiple MIB regions.
* Multiple MIB update classes with custom frequency for each.
* Support snmpset operations.
* Reconnect/Retry to master, in case the master restarted.


## Installation

The package is registered on [Python Package Index](https://pypi.python.org/) under the name  "pyagentx2" [https://pypi.python.org/pypi/pyagentx2](https://pypi.python.org/pypi/pyagentx2).

You can install it by simply running:

    pip install pyagentx2

## SNMP Agent Configuration

I have tested the pyagentx with NetSNMP, using [this](https://hub.docker.com/r/jslarraz/netsnmp) docker image. If you use this container, you can configure the NetSNMP agent according to its documentation.

## Change log

Changes from the origina pyagentx:
* fix an error regarding ip address data type (encoding/decoding was wrong)
* mib management has been decoupled from network functionality (created new MIB class)
* set handlers now also receive the data type of the value and the mib object
* use shared memory for inter-thread communication instead of queues.
* support for python3
* support for different error during testset