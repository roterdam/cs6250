#!/usr/bin/python

"Assignment 6 - This creates the firewall policy. "

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.modules.dns_firewall import *

class Firewall(DynamicPolicy):

    def __init__(self):
        # Init the parent class.
        super(Firewall,self).__init__()
        self.network = None
        self.set_policy()

    # This calls the student defined function in dns_firewall.py, then sends
    # the packed based on what was returned by the student function.
    def dns_callback(self, pkt):
        snd = dns_firewall(pkt)
        if snd is not None:
            # Switch is always 1 in this case.
            switch = 1
            # Get the other port:
            if snd['inport'] == 1:
                port = 2
            else:
                port = 1
            self.send_packet(switch, port, snd)
        

    def set_policy(self):
        # This is the default policy for the firwall switch. Non-DNS packets
        # get forwarded automatically, DNS packets go through the student code.
        non_dns_traffic = ~match(ethtype=2048, protocol=17, srcport = 53) >> ~match(ethtype=2048, protocol=17, dstport = 53) >> flood()
        
        # Getting all DNS traffic.
        dnspkts = packets(None, ['srcmac'])
        dnspkts.register_callback(self.dns_callback)
        dns_inbound = match(ethtype=2048, protocol=17, srcport = 53) >> dnspkts
        dns_outbound = match(ethtype=2048, protocol=17, dstport = 53) >> dnspkts
    
        # Compose the subpolicies for Non-DNS traffic and for capturing the 
        # DNS traffic and forwarding to the appropriate locations
        # self.policy is a special variable. 
        self.policy = non_dns_traffic + dns_inbound + dns_outbound


    # Helper functions:

    # This is part of the DynamicPolicy parent class. It is called when there 
    # is a network change event. In our setup, this will only happen once: 
    # at startup.
    def set_network(self, network):
        self.network = network

    # This sends packets. You need to provide where it's being sent from. 
    # For our case, switch should always equal 1.
    def send_packet(self, switch, port, pkt):
        rp = pkt
        rp = rp.modify(switch = switch)
        rp = rp.modify(inport = -1)
        rp = rp.modify(outport = port)

        self.network.inject_packet(rp)
