#!/usr/bin/python

"Assignment 5 - This is the controller that implements a firewall loaded \
    from a configuration file. Like Assignment 2, it is Pyretic based. \
    Scattered borrowing from Spring 2015 Assignment 7."
   

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.modules.pyretic_switch import ActLikeSwitch
from pyretic.modules.firewall_policy import make_firewall_policy
import re
import os


policy_file = "%s/pyretic/pyretic/modules/firewall-policies.cfg" % os.environ[ 'HOME' ]

def main():
    """ Initialization of the Firewall. This pulls its rules from the file
            defined above. You can change this file pointer, but be sure to 
            change it back before submission! The run-firewall.sh file copies 
            over both this file and the configuration file to the correct 
            location."""
        
    # Parse the input file - make sure it's valid.
    config = parse_config(policy_file)
    
    # Get learning switch module
    learningSwitch = ActLikeSwitch()
    
    # Make Firewall policy
    fwPolicy = make_firewall_policy(config)
    
    # Return composed policy
    return fwPolicy >> learningSwitch




def parse_config(filename):
    with open(filename, 'r') as f:
        policies = []
        for line in f:
            # Skip if it's a comment (begins with #) or empty
            if re.match("#.*", line.strip()) != None:
                continue
            cleanline = ''.join(line.split())
            if cleanline == '':
                continue

            # Check that it's valid
            if len(cleanline.split(',')) != 7:
                raise TypeError("There are only %i parts to the line \"%s\"; there must be 7."
                                % (len(cleanline.split(',')), line))

            (rulenum, srcmac, dstmac, srcip, dstip, 
             srcport, dstport) = cleanline.split(',')
            
            
            if (srcmac != '*' and
                None == re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", 
                                 srcmac.lower())):
                raise TypeError("srcmac for rule %s is invalid" % rulenum)
            if (dstmac != '*' and
                None == re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", 
                                 dstmac.lower())):
                raise TypeError("dstmac for rule %s is invalid" % rulenum)
            
            if (srcip != '*' and not valid_ip(srcip)):
                raise TypeError("srcip for rule %s is invalid" % rulenum)                
            if (dstip != '*' and not valid_ip(dstip)):
                raise TypeError("dstip for rule %s is invalid" % rulenum)                
                
            if (srcport != '*' and (int(srcport) > 65535 or int(srcport) < 1)):
                raise TypeError("srcport for rule %s is invalid" % rulenum)                
            if (dstport != '*' and (int(dstport) > 65535 or int(dstport) < 1)):
                raise TypeError("dstport for rule %s is invalid" % rulenum)                
                
            # Add it to the policies structure
            pol = {'rulenum':rulenum,
                   'srcmac':srcmac,
                   'dstmac':dstmac,
                   'srcip':srcip,
                   'dstip':dstip,
                   'srcport':srcport,
                   'dstport':dstport}
            policies.append(pol)

        return policies

# from https://stackoverflow.com/questions/11264005/using-a-regex-to-match-ip-addresses-in-python
def valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False
