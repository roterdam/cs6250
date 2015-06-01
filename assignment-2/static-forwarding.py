#!/usr/bin/python

" Assignment 2 - static-forwarding.py - \
    First part of the assignment. This is to create a static-forwarding table. \
 student: Ngoc (Amy) Tran - Assignment 2 - Part 1- static switching "


from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from helpers import *


class StaticSwitch(Policy):
    def __init__(self):
        """ 
        Initialization of static switch. Set up your forwarding tables  here.
        You need to key off of Switch and MAC address to determine forwarding
        port.
        Suggested routes: 
          - Array with switch as index, dictionary for MAC to switch port
          - dictionary of dictionaries
        """

        # Initialize the parent class
        super(StaticSwitch, self).__init__()

        # TODO: set up forwarding tables. Create this however you wish. As
        # a suggestion, using a list of tuples will work.
        # Create the static forwarding table
        #self.forward_table_list = []
        self.forward_table = []
        # Create table with switchnum, macaddr, and switchport
        # use append to add item to the list
        # The list for Switch A = S1
        self.forward_table.append((1, 1, "00:00:00:00:00:01"))
        self.forward_table.append((1, 2, "00:00:00:00:00:02"))
        # between the switches
        self.forward_table.append((1, 3, "00:00:00:00:00:03"))
        self.forward_table.append((1, 3, "00:00:00:00:00:04"))
        # The list for Switch B = S2
        self.forward_table.append((2, 3, "00:00:00:00:00:01"))
        self.forward_table.append((2, 3, "00:00:00:00:00:02"))
        # S2 connected to H3 and H4
        self.forward_table.append((2, 1, "00:00:00:00:00:03"))
        self.forward_table.append((2, 2, "00:00:00:00:00:04"))

        # Create log file switches table for grading
        self.logfile_static_fw_tables()

    def logfile_static_fw_tables(self):
        # TODO: Create log file "static-forwarding.log"
        open_log("static-forwarding.log")
        for tb_item in self.forward_table:
            write_forwarding_entry(tb_item[0], tb_item[1], tb_item[2])
        # close log file
        finish_log()
        print "** finished the log file"


    def build_policy(self):
        """ 
        This creates the pyretic policy. You'll need to base this on how you 
        created your forwarding tables. You need to compose the policies 
        in parallel. 
        """

        # TODO: Rework below based on how you created your forwarding tables.
        
        subpolicies = []
        # switch_1 port 1 & 2 connected to h1 and h2
        subpolicies.append(match(switch=1, dstmac="00:00:00:00:00:01") >> fwd(1))
        subpolicies.append(match(switch=1, dstmac="00:00:00:00:00:02") >> fwd(2))
        # between the switches 1 & 2
        subpolicies.append(match(switch=1, dstmac="00:00:00:00:00:03") >> fwd(3))
        subpolicies.append(match(switch=1, dstmac="00:00:00:00:00:04") >> fwd(3))
         # switch_2 h3 and h4
        subpolicies.append(match(switch=2, dstmac="00:00:00:00:00:03") >> fwd(1))
        subpolicies.append(match(switch=2, dstmac="00:00:00:00:00:04") >> fwd(2))
        # between the switches 2 & 1
        subpolicies.append(match(switch=2, dstmac="00:00:00:00:00:01") >> fwd(3))
        subpolicies.append(match(switch=2, dstmac="00:00:00:00:00:02") >> fwd(3))
        ## Completed the forwarding table policies


        # NOTE: this will flood for MAC broadcasts (to ff:ff:ff:ff:ff:ff).
        # You will need to include something like this in order for ARPs to 
        # propogate. xfwd() is like fwd(), but will not forward out a port a 
        # packet came in on. Useful in this case.
        subpolicies.append(match(switch=1, dstmac="ff:ff:ff:ff:ff:ff") >> parallel([xfwd(1), xfwd(2), xfwd(3)]))
        subpolicies.append(match(switch=2, dstmac="ff:ff:ff:ff:ff:ff") >> parallel([xfwd(1), xfwd(2), xfwd(3)]))

        # This returns a parallel composition of all the subpolicies you put
        # together above.
        return parallel(subpolicies)
            
        
        
        
def main():
    return StaticSwitch().build_policy()
