import pytest
import subprocess

## Sets

@pytest.fixture
def set_cmd():
    return ["snmpset", "-v", "2c", "-c", "private", "localhost"]

@pytest.fixture
def get_cmd():
    return ['snmpget', '-v', '2c', '-c', 'private', 'localhost']

@pytest.fixture
def walk_cmd():
    return ['snmpwalk', '-v', '2c', '-c', 'private', 'localhost']



def test_set_integer(set_cmd):
    output = subprocess.check_output(set_cmd + ['1.3.6.1.4.1.8072.2.1.1.0', 'i', '1'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.1.0 = INTEGER: 1\n'
#
def test_set_octect_string(set_cmd):
    output = subprocess.check_output(set_cmd + ['1.3.6.1.4.1.8072.2.1.2.0', 's', 'TESTSTRING'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.2.0 = STRING: "TESTSTRING"\n'
#
def test_set_ip_address(set_cmd):
    output = subprocess.check_output(set_cmd + ['1.3.6.1.4.1.8072.2.1.3.0', 'a', '255.255.255.255'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.3.0 = IpAddress: 255.255.255.255\n'


## Gets

def test_get_integer(get_cmd):
    output = subprocess.check_output(get_cmd + ['1.3.6.1.4.1.8072.2.1.1.0'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.1.0 = INTEGER: 1\n'
#
def test_get_octect_string(get_cmd):
    output = subprocess.check_output(get_cmd + ['1.3.6.1.4.1.8072.2.1.2.0'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.2.0 = STRING: "TESTSTRING"\n'
#
def test_get_ip_address(get_cmd):
    output = subprocess.check_output(get_cmd + ['1.3.6.1.4.1.8072.2.1.3.0'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.3.0 = IpAddress: 255.255.255.255\n'

def test_walk(walk_cmd):
    output = subprocess.check_output(walk_cmd + ['1.3.6.1.4.1.8072.2.1'])
    assert output.decode() == 'iso.3.6.1.4.1.8072.2.1.1.0 = INTEGER: 1\niso.3.6.1.4.1.8072.2.1.2.0 = STRING: "TESTSTRING"\niso.3.6.1.4.1.8072.2.1.3.0 = IpAddress: 255.255.255.255\niso.3.6.1.4.1.8072.2.1.4.0 = OID: iso.2\niso.3.6.1.4.1.8072.2.1.5.0 = IpAddress: 127.0.0.1\niso.3.6.1.4.1.8072.2.1.6.0 = Counter32: 2000\niso.3.6.1.4.1.8072.2.1.7.0 = Gauge32: 2000\niso.3.6.1.4.1.8072.2.1.8.0 = Timeticks: (1000000) 2:46:40.00\niso.3.6.1.4.1.8072.2.1.9.0 = OPAQUE: 54 65 73 74 \niso.3.6.1.4.1.8072.2.1.10.0 = Counter64: 2000\n'