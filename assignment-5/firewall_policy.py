#!/usr/bin/python

"Assignment 5 - This creates the firewall policy. "

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core.packet import IPV4, TCP_PROTO
from collections import namedtuple

Policy = namedtuple('Policy', ('srcmac', 'dstmac','srcip','dstip','srcport','dstport'))

def make_firewall_policy(config):
    # TODO - This is where you need to write the functionality to create the
    # firewall. What is passed in is a list of rules that you must implement
    # using the Pyretic syntax that was used in Assignment 2. 

    # feel free to remove the following "print config" line once you no longer need it
    #print "***Amy print config:"
    #print config # for demonstration purposes only, so you can see the format of the config
    fwpolicies = make_firewall_list(config)

    if (fwpolicies.__len__() < 1):
        raise TypeError("Error! Not found firewall policy...\n")

    rules = []
    for policy in fwpolicies.itervalues():
        # TODO - build the individual rules
        rule = add_firewall_rule(policy)
        rules.append(rule)
        pass

    allowed = ~(union(rules))
    print "====Allowed:===\n"
    print allowed 
   
    return allowed

def make_firewall_list(config):
    # Create a list of firewall policy
    policy_list = {}
    for entry in config:
        policy_list [entry['rulenum']] = Policy(entry['srcmac'], entry['dstmac'],
                                                entry['srcip'], entry['dstip'],
                                                entry['srcport'], entry['dstport'])
        values = policy_list.values()
    return policy_list

def add_firewall_rule(policy):
    # start with default rule
    rule = match(ethtype=IPV4, protocol=TCP_PROTO)

    if (block_all(policy) == true):
        print "*NOTE: +++You block all ports+++ ****"
        rule = match(ethtype=IPV4, protocol=TCP_PROTO)
    else:
        #Check srcmac and dstmac
        if ((policy.srcmac != '*') and (policy.dstmac != '*')):
            rule = match(srcmac = EthAddr(policy.srcmac), dstmac = EthAddr(policy.dstmac))
        elif (policy.srcmac != '*'):
            rule = match(srcmac = EthAddr(policy.srcmac))
        elif (policy.dstmac != '*'):
            rule = match(dstmac = EthAddr(policy.dstmac))

        # Check both dstport & srcport
        if (policy.dstport != '*'):
            rule = rule & match(dstport = int(policy.dstport))
        if (policy.srcport != '*'):
            rule = rule & match(srcport = int(policy.srcport))

        # check both srcip and dstip
        if ((policy.srcip != '*') and (policy.dstip != '*')):
            rule = rule & match(srcip = IPAddr(policy.srcip), dstip=IPAddr(policy.dstip))
        elif (policy.dstip != '*'):
            rule = rule & match(dstip = IPAddr(policy.dstip))
        elif (policy.srcip != '*'):
            rule = rule & match(dstip = IPAddr(policy.srcip))

    return rule


def block_all(policy):
    if (policy.srcmac == '*' and policy.dstmac == '*' \
        and policy.srcip == '*' and policy.dstip == '*' \
        and policy.srcport == '*' and policy.dstport == '*'):
        print "**** Block all ports****"
        return True
    else:
        return False



