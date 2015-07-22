#!/usr/bin/python

"Assignment 6 - This defines a topology for creating DNS Amplification \
    attacks, and for creating a firewall that blocks them."

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.util import custom
from mininet.link import TCLink
from mininet.cli  import CLI

class FWTopo(Topo):
    ''' Creates the following topoplogy:
         svr
          |
          |
      firewall (s1)
          |
          |
      swtich (s2)
      /   |   \
     |    |    |
    h1    h2   dns
    '''
    def __init__(self, cpu=.1, bw=2.0, delay=None, **params):
        super(FWTopo,self).__init__()
        
        # Host in link configuration
        hconfig = {'cpu': cpu}
        fat_lconfig = {'bw': bw, 'delay': delay}
        med_lconfig = {'bw': bw/2.0, 'delay': delay}
        skinny_lconfig = {'bw': bw/6.0, 'delay': delay}
        
        # Create the firewall switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        
        # Create East hosts and links)
        dns = self.addHost('dns', **hconfig)
        h1 = self.addHost('h1', **hconfig)
        h2 = self.addHost('h2', **hconfig)
        svr = self.addHost('svr', **hconfig)
        self.addLink(s1, svr, port1=2, port2=1, **med_lconfig)
        self.addLink(s1, s2, port1=1, port2=1, **fat_lconfig)
        self.addLink(s2, dns, port1=3, port2=1, **med_lconfig)
        self.addLink(s2, h1, port1=4, port2=1, **skinny_lconfig)
        self.addLink(s2, h2, port1=5, port2=1, **skinny_lconfig)


def start_webserver(svr):
    svr.cmd('cd ./http/; nohup python2.7 ./webserver.py &')
    svr.cmd('cd ../')


def stop_webserver(svr):
    svr.cmd("sudo pkill -9 -f webserver.py")
    svr.cmd("rm -f http/nohup.out")


def start_dns(dns):
    dns.cmd('service bind9 restart')


def stop_dns(dns):
    dns.cmd('service bind9 stop')


def main():
    print "Starting topology"
    topo = FWTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController, autoSetMacs=True)

    net.start()
    start_dns(net.getNodeByName('dns'))
    start_webserver(net.getNodeByName('svr'))

    CLI(net)
    stop_webserver(net.getNodeByName('svr'))
    stop_dns(net.getNodeByName('dns'))
    net.getNodeByName('h2').cmd("rm -f index.html*")

if __name__ == '__main__':
    main()
