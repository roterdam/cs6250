#!/usr/bin/python

"Assignment 5 - This is the controller that implements a firewall loaded \
    from a configuration file. Like Assignment 2, it is Pyretic based. \
    Scattered borrowing from Spring 2015 Assignment 7."
   

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.pyretic_switch import ActLikeSwitch
from pyretic.modules.firewall import *

def main():
    """ Initialization of the Firewall. This pulls its rules from the file
            defined above. You can change this file pointer, but be sure to 
            change it back before submission! The run-firewall.sh file copies 
            over both this file and the configuration file to the correct 
            location."""
        
    # Get firewall policy
    firewall = Firewall()

    # Get learning switch module
    learningSwitch = ActLikeSwitch()

    # Create subpolicies
    sw1_policy = match(switch=1) >> firewall
    sw2_policy = match(switch=2) >> learningSwitch

    # Return composed policy
    return sw1_policy + sw2_policy


