#!/usr/bin/python

"Assignment 6 - Student functionality."

from ryu.lib.packet import dns




# TODO: You should declare your global variables here. 
DNS_OFFSET = 42


# This function receives all DNS packets that are received by the switch.
# Parsing code has already been provided, so you must decide on what to do
# to satisfy the requirements of the assignment. 
def dns_firewall(pkt):
    # WARNING: be careful of any print statements or other output in this fn
    #    output here will *destroy* performance during at attack, due to the
    #    large number of packets processed and the time required to print you
    #    can use some temporarily for debugging, but be sure to remove /
    #    comment them out before running to check performance (or turning in!)

    # Adjust for the offset of the beginning of DNS data in the packet to
    # the end of the packet (the : afterwards).
    packet = pkt['raw'][DNS_OFFSET:]
    
    # This is defined in pyretic/pyretic/vendor/ryu/ryu/lib/packet/dns.py,
    # also in assignment-6/ryu_update/dns.py
    dns_parsed = dns.dns.parser(packet)


    # The next three items you will probably need to use to properly implement
    # This assignment:

    # This is the Query flag. True = response. False = query
    query_flag = dns_parsed.qr

    # This is the transaction ID, which is how responses and requests can be
    # matched up (they will have the same transaction ID)
    transaction_ID = dns_parsed.id

    # questions will be a list of all the queries that are made in the request.
    questions = dns_parsed.questions


    # TODO: Implement your code here. Return pkt if the packet should be 
    # forwarded, or return None if it should be dropped.
    # You will need to keep track of the appropriate information (in a 
    # locally global structure - see the top of the file), then process
    # the packets that come through.


    return pkt # default policy = allow all; you should change this

    
    
