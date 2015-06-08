#!/usr/bin/python

"Assignment 4 - This is the controller code that students will have to \
    implement sections of. It is Pyretic based, but this is somewhat\
    unimportant at the moment, as we only care about the learning\
    behaviors.\
    Student: Ngoc (Amy) Tran - Assignment 2 - Part2- Learn Switch. "

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from helpers import *


class LearningSwitch(DynamicPolicy):
    def __init__(self):
        """ Initialization of the Learning Switch. The important piece
            is the definition of the switch mapping. This is a nested
            dictionary. """

        # Initialize the parent class
        super(LearningSwitch, self).__init__()

        # TODO: Initialize your forwarding tables. Create this however you wish.
        # Couple of suggestions: Dictionary of dictionaries, Dictionary of
        # tuples.
        # initialize the forwarding table to empty.
        # base on the learn-swtch-topo, it has s1->s5
        self.forward_table = {}
        # the s1-s5 switch fw table
        self.forward_table[1] = {}
        self.forward_table[2] = {}
        self.forward_table[3] = {}
        self.forward_table[4] = {}
        self.forward_table[5] = {}

        # only use one flood instance - this is the default policy when there
        # isn't a known path.
        self.flood = flood()

        # Get the first packet from each new MAC address on a switch. This
        # is how we are able to learn new routes.
        new_pkts = packets(1, ['srcmac', 'switch'])
        new_pkts.register_callback(self.learn_route)
        self.query = new_pkts

        # Initialize the policy
        self.build_policy()


    def print_switch_tables(self):
        # TODO - You will need to implement this based on how your forwarding
        # table are set up. Us the functions in the first half of helpers.
        # Format should be to call write_forwarding_entry() for each entry in
        # the forwarding table, then finish up with finish_printing().
        open_log("learning-switch.log")
        for switch_num in self.forward_table.keys():
            for mac_num in self.forward_table[switch_num].keys():
                write_forwarding_entry(switch_num, self.forward_table[switch_num][mac_num],str(mac_num))
            next_entry()
        finish_log()

    def learn_route(self, pkt):
        """  This function adds new routes into the fowarding table. """

        # TODO - create a new entry in the fowarding table. Use the functions
        # in the second half of helpers to simplify all your work.
        # the forwarding table.
        #  Extract the correct pieces from the packet to populate
        # the forwarding table.
        ''' For Debug forward table
        switchnum = get_switch(pkt)
        mac_addr = get_src_mac(pkt)
        port_info = get_inport(pkt)

        # The forwarding table
        self.forward_table[switchnum][mac_addr] = port_info
        ''' #End of the debug

        # The forwarding table
        self.forward_table[get_switch(pkt)][get_src_mac(pkt)] = get_inport(pkt)

        # print out the switch tables:
        self.print_switch_tables()

        # Call build_policy to update the fowarding tables of the switches.
        self.build_policy()
        pass


    def build_policy(self):
        """
        This is similar to the build_policy() function in StaticSwitch.
        There is a major difference: If there isn't a rule, you need to flood
        the packets. The example code should help.
        """
        new_policy = None
        not_flood_pkts = None


        # TODO: Example code. You will need to edit this based on how you're
        # storing your policies. You should only have to replace the details in
        # rule entries.
        #rule1 = 1, "00:00:00:00:00:01", 3
        #rule2 = 1, "00:00:00:00:00:02", 2
        for switch_num in self.forward_table.keys():
            for rule in self.forward_table[switch_num].keys():
                if new_policy == None:
                    # First entry, prime the pump
                    new_policy = (match(switch=int(switch_num), dstmac=rule) >>
                                  fwd(self.forward_table[switch_num][rule]))
                else:
                    new_policy += (match(switch=int(switch_num), dstmac=rule) >>
                                   fwd(self.forward_table[switch_num][rule]))

                if not_flood_pkts == None:
                    not_flood_pkts = (match(switch=int(switch_num), dstmac=(rule)))
                else:
                    not_flood_pkts |= (match(switch=int(switch_num), dstmac=(rule)))


        # If you follow the pattern above, you won't have to change this below.
        # We don't know of any rules yet, so flood everything.
        if not_flood_pkts == None:
            self.policy = self.flood + self.query
        else:
            self.policy = if_(not_flood_pkts, new_policy, self.flood) + self.query

        # The following line can be uncommented to see your policy being
        # built up, say during a flood period.
        # print self.policy


def main():
    return LearningSwitch()