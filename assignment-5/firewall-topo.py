#!/usr/bin/python

"Assignment 5 - This defines a topology for running a firewall. It is not \
    necessarily the topology that will be used for grading, so feel free to \
    edit and create new topologies and share them."

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.util import custom
from mininet.link import TCLink
from mininet.cli  import CLI

class FWTopo(Topo):
    ''' Creates the following topoplogy:
     e1   e2   e3
     |    |    |
      \   |   /
      firwall (s1)
      /   |   \
     |    |    |
    w1    w2   w3
    '''
    def __init__(self, cpu=.1, bw=10, delay=None, **params):
        super(FWTopo,self).__init__()
        
        # Host in link configuration
        hconfig = {'cpu': cpu}
        lconfig = {'bw': bw, 'delay': delay}
        
        # Create the firewall switch
        s1 = self.addSwitch('s1')
        
        # Create East hosts and links)
        e1 = self.addHost('e1', **hconfig)
        e2 = self.addHost('e2', **hconfig)
        e3 = self.addHost('e3', **hconfig)
        self.addLink(s1, e1, port1=1, port2=1, **lconfig)
        self.addLink(s1, e2, port1=2, port2=1, **lconfig)
        self.addLink(s1, e3, port1=3, port2=1, **lconfig)
        
        # Create West hosts and links)
        w1 = self.addHost('w1', **hconfig)
        w2 = self.addHost('w2', **hconfig)
        w3 = self.addHost('w3', **hconfig)
        self.addLink(s1, w1, port1=4, port2=1, **lconfig)
        self.addLink(s1, w2, port1=5, port2=1, **lconfig)
        self.addLink(s1, w3, port1=6, port2=1, **lconfig)


def main():
    print "Starting topology"
    topo = FWTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController, autoSetMacs=True)

    net.start()
    CLI(net)

if __name__ == '__main__':
    main()
