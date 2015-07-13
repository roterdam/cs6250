#Author Pico Geyer
#Contributors:
# Robert Moe

import time
import re
import random
import os.path

class SetupError(Exception): pass
class TestFailure(Exception): pass

required_hosts = ['e1', 'e2', 'e3', 'w1', 'w2', 'w3']

tools_path=''

#Implementation of tests.
#Each test should clean up after itself so as not to affect the other tests

def block_east_west_port_1080(mn):
    print "***********************************************************************************"
    print "TEST: 'Block all traffic in both directions between the East and West on port 1080'"
    print "***********************************************************************************"
    failed = False

    port = 1080

    east = ['e1', 'e2', 'e3']
    west = ['w1', 'w2', 'w3']

    # Test East to West
    for e in east:
        for w in west:
            if testconnection(mn, w, e, port):
                failed = True
                print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format(e, w, port)
            else:
                print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format(e, w, port)

    # Test West to East
    for w in west:
        for e in east:
            if testconnection(mn, e, w, port):
                failed = True
                print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format(w, e, port)
            else:
                print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format(w, e, port)

    if failed:
        raise TestFailure("FAILED: 'Block all traffic in both directions between the East and West on port 1080'")
    else:
        print "PASSED: 'Block all traffic in both directions between the East and West on port 1080'"

def block_e1_to_w1_completely(mn):
    print "***********************************************************************************"
    print "TEST: 'Block e1 from communicating with w1 completely in both directions'"
    print "***********************************************************************************"

    # Pick 20 random numbers between port 1024 and 10000
    ports = random.sample(xrange(1024, 10000), 20)

    failed = False

    # Test East To West
    for port in ports:
        if testconnection(mn, 'w1', 'e1', port):
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('e1', 'w1', port)
        else:
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('e1', 'w1', port)

    # Test West To East
    for port in ports:
        if testconnection(mn, 'e1', 'w1', port):
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('w1', 'e1', port)
        else:
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('w1', 'e1', port)

    if failed:
        raise TestFailure("FAILED 'Block e1 from communicating with w1 completely in both directions'")
    else:
        print "PASSED: 'Block e1 from communicating with w1 completely in both directions'"

def block_e2_to_w2_over_2000(mn):
    print "***********************************************************************************"
    print "TEST: 'Block e2 from communicating with w2 over ports 2000-2004 in both directions'"
    print "***********************************************************************************"

    failed = False

    ports = list(xrange(2000, 2005))

    # Test East To West
    for port in ports:
        if testconnection(mn, 'w2', 'e2', port):
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('e2', 'w2', port)
        else:
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('e2', 'w2', port)

    # Test West To East
    for port in ports:
        if testconnection(mn, 'e2', 'w2', port):
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('w2', 'e2', port)
        else:
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('w2', 'e2', port)

    if failed:
        raise TestFailure("FAILED 'Block e2 from communicating with w2 over ports 2000-2004 in both directions'")
    else:
        print "PASSED: 'Block e2 from communicating with w2 over ports 2000-2004 in both directions'"


def allow_traffic_within_east_west(mn):
    print "***********************************************************************************"
    print "TEST: 'Allow all traffic within the East or West sites to port 1234'"
    print "***********************************************************************************"
    failed = False

    #port = 1080
    port = 1234

    east = ['e1', 'e2', 'e3']
    west = ['w1', 'w2', 'w3']

    # Test East Container
    for e in east:
        for e1 in east:
            if e != e1:
                if testconnection(mn, e, e1, port):
                    print 'PASS: Connection established from client ({}) to server ({}) on port ({})'.format(e1, e, port)
                else:
                    failed = True
                    print 'FAIL: Connection could not be established from client ({}) to server ({}) on port ({})'.format(e1, e, port)

    # Test West Container
    for w in west:
        for w1 in west:
            if w != w1:
                if testconnection(mn, w, w1, port):
                    print 'PASS: Connection established from client ({}) to server ({}) on port ({})'.format(w1, w, port)
                else:
                    failed = True
                    print 'FAIL: Connection could not be established from client ({}) to server ({}) on port ({})'.format(w1, w, port)

    if failed:
        raise TestFailure("FAILED: 'Allow all traffic within the East or West sites to port 1080'")
    else:
        print "PASSED: 'Allow all traffic within the East or West sites to port 1080'"

def block_e3_to_w3_over_3000(mn):
    print "***********************************************************************************"
    print "TEST: 'Block e3 from communicating with w3 over ports 3000-3002'"
    print "***********************************************************************************"

    failed = False

    ports = list(xrange(3000, 3003))

    # Test East To West
    for port in ports:
        if testconnection(mn, 'w3', 'e3', port):
            failed = True
            print 'FAIL: Connection established from client ({}) to server ({}) on port ({})'.format('e3', 'w3', port)
        else:
            print 'PASS: Connection refused from client ({}) to server ({}) on port ({})'.format('e3', 'w3', port)

    # Test West To East
    for port in ports:
        if testconnection(mn, 'e3', 'w3', port):
            print 'PASS: Connection established from client ({}) to server ({}) on port ({})'.format('w3', 'e3', port)
        else:
            failed = True
            print 'FAIL: Connection refused from client ({}) to server ({}) on port ({})'.format('w3', 'e3', port)

    if failed:
        raise TestFailure("FAILED 'Block e3 from communicating with w3 over ports 3000-3002'")
    else:
        print "PASSED: 'Block e3 from communicating with w3 over ports 3000-3002'"

def testconnection(mn, server, client, port):

    client_host = mn.get(client)
    server_host = mn.get(server)

    client_IP = client_host.IP()
    server_IP = server_host.IP()

    print 'Starting server ({}) on {}:{}'.format(server, server_IP, port)
    server_host.sendCmd('python {} {} {}'.format(
        os.path.join(tools_path, 'test-server.py'),
        server_IP,
        int(port)),
        printPid=True)
    time.sleep(1)

    print 'Starting client ({}) connecting to {}:{}'.format(client, server_IP, port)
    client_host.sendCmd('python {} {} {}'.format(
        os.path.join(tools_path, 'test-client.py'),
        server_IP,
        int(port)),
        printPid=True)
    time.sleep(1)

    client_host.sendInt()
    server_host.sendInt()

    client_data = client_host.monitor()
    server_data = server_host.monitor()

    client_host.waiting = server_host.waiting = False

    if 'received' in client_data:
        return True
    return False

def check_hosts(mn):
    missing_host = False
    for r in required_hosts:
        try:
            mn.get(r)
        except KeyError:
            print 'Required host {} seems to be missing from the topology'.format(r)
            missing_host = True
    if missing_host:
        raise SetupError("Missing hosts")

def check_setup():
    #Make sure we can find our tools
    global tools_path
    #first check for tools in current dir
    if os.path.exists('test-client.py'):
        tools_path=os.path.abspath('.')
    elif os.path.exists('../test-client.py'):
        tools_path=os.path.abspath('..')
    else:
        raise SetupError('Can\'t find testing tools')

def run_tests(mn):
    #list of tests to run, edit as needed
    tests = ['block_east_west_port_1080',
             'block_e1_to_w1_completely',
             'allow_traffic_within_east_west',
             'block_e2_to_w2_over_2000',
             'block_e3_to_w3_over_3000']
    #first do a sanity check
    check_hosts(mn)
    check_setup()
    mn.pingAll()
    for t in tests:
        to = globals()[t]
        try:
            to(mn)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print str(e)
