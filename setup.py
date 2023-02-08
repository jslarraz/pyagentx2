from setuptools import setup


setup(
    name = "pyagentx2",
    version = "1.0.15",
    author = "Jorge Sancho",
    author_email = "jslarraz@gmail.com",
    description = ("AgentX package to extend SNMP with pure Python"),
    license = "BSD",
    keywords = "snmp network agentx ",
    url = "https://github.com/jslarraz/pyagentx2",
    packages=['pyagentx2'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Environment :: No Input/Output (Daemon)",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
    ],
    long_description='''\
PyAgentX2
--------------------
pyagentx2 is a fork of pyagentx, which is a pure Python implementation of AgentX protocol (RFC 2741), that
allows you to extend SNMP agent (snmpd) by writing AgentX subagents, without modifying your original SNMP agent.

The agent can support the following commands:
- snmpget
- snmpwalk
- snmptable
- snmpset

''',
)
