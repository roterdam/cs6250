# Copyright (C) 2014 Sean Donovan
# Copyright (C) 2012 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# vim: tabstop=4 shiftwidth=4 softtabstop=4

import unittest
import logging
import struct
from struct import *
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from ryu.ofproto import ether
from ryu.lib.packet.ethernet import ethernet
from ryu.lib.packet.packet import Packet
from ryu.lib.packet.dns import *
from ryu.lib.packet.vlan import vlan
from ryu.lib import addrconv


LOG = logging.getLogger('test_dns')


class Test_dns(unittest.TestCase):
    """ Test case for dns
    """

    hwtype = 1
    proto = ether.ETH_TYPE_IP

    id = 0xEDA7
    qr = False
    opcode = 0
    aa = False
    tc = False
    rd = True
    ra = True
    z = False
    ad = False
    cd = False
    rcode = 0

    # assume the questions and rr utility classes works
    questions = []
    answers = []
    authorities = []
    additional = []

    questions.append(dns.question("seandonovan.net", 1, 1))

    answers.append(dns.rr("seandonovan.net", 1, 1, 0x00000E10, 4, addrconv.ipv4.text_to_bin("208.94.117.114")))
    answers.append(dns.rr("seandonovan.net", 1, 1, 0x00000E10, 4, addrconv.ipv4.text_to_bin("208.94.116.135")))
    answers.append(dns.rr("seandonovan.net", 1, 1, 0x00000E10, 4, addrconv.ipv4.text_to_bin("208.94.117.13")))
    
    authorities.append(dns.rr("seandonovan.net", 2, 1, 0x00000E10, 27, "ns.phx1.nearlyfreespeech.net"))
    authorities.append(dns.rr("seandonovan.net", 2, 1, 0x00000E10, 27, "ns.phx2.nearlyfreespeech.net"))

    additional.append(dns.rr("ns.phx1.nearlyfreespeech.net", 1, 1, 0x0000f560, 4, addrconv.ipv4.text_to_bin("208.94.116.1")))
    additional.append(dns.rr("ns.phx2.nearlyfreespeech.net", 1, 1, 0x0000f560, 4, addrconv.ipv4.text_to_bin("208.94.116.33")))


    bits0 = 0
    if qr: bits0 |= 0x80
    bits0 |= (opcode & 0x7) << 4
    if rd: bits0 |= 1
    if tc: bits0 |= 2
    if aa: bits0 |= 4
    bits1 = 0
    if ra: bits1 |= 0x80
    if z: bits1 |= 0x40
    if ad: bits1 |= 0x20
    if cd: bits1 |= 0x10
    bits1 |= (rcode & 0xf)

    buf = struct.pack("!HBBHHHH", id, bits0, bits1, len(questions),
                      len(answers), len(authorities), len(additional))
    name_map = {}
    for r in questions:
        buf = putName(buf, r.name, name_map)
        buf += struct.pack("!HH", r.qtype, r.qclass)

    rest = answers + authorities + additional
    for r in rest:
        buf = putName(buf, r.name, name_map)
        buf += struct.pack("!HHIH", r.qtype, r.qclass, r.ttl, 0)
        fixup = len(buf) - 2
        buf = putData(buf, r, name_map)
        fixlen = len(buf) - fixup - 2
        buf = buf[:fixup] + struct.pack('!H', fixlen) + buf[fixup+2:]


#    a = arp(hwtype, proto, hlen, plen, opcode, src_mac, src_ip, dst_mac,
#            dst_ip)

#    a = dns()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def find_protocol(self, pkt, name):
        for p in pkt.protocols:
            if p.protocol_name == name:
                return p

    def test_init(self):
        pass

#        eq_(self.hwtype, self.a.hwtype)
#        eq_(self.proto, self.a.proto)
#        eq_(self.hlen, self.a.hlen)
#        eq_(self.plen, self.a.plen)
#        eq_(self.opcode, self.a.opcode)
#        eq_(self.src_mac, self.a.src_mac)
#        eq_(self.src_ip, self.a.src_ip)
#        eq_(self.dst_mac, self.a.dst_mac)
#        eq_(self.dst_ip, self.a.dst_ip)
    
    def runTest(self):
        self.test_parser()
        self.test_serialize()
        print "Successfully tested parser and serializer."


    def test_parser(self):
        _res = dns.parser(self.buf)
        if type(_res) is tuple:
            res = _res[0]
        else:
            res = _res

        eq_(res.hwtype, self.hwtype)
        eq_(res.proto, self.proto)
        eq_(res.id, self.id)
        eq_(res.qr, self.qr)
        eq_(res.opcode, self.opcode)
        eq_(res.aa, self.aa)
        eq_(res.tc, self.tc)
        eq_(res.rd, self.rd)
        eq_(res.ra, self.ra)
        eq_(res.z, self.z)
        eq_(res.ad, self.ad)
        eq_(res.cd, self.cd)
        eq_(res.rcode, self.rcode)
        
        eq_(len(res.questions), len(self.questions))

        for (r,s) in zip(res.questions, self.questions):
            eq_(r.name, s.name)
            eq_(r.qtype, s.qtype)
            eq_(r.qclass, s.qclass)
        
        eq_(len(res.answers), len(self.answers))
        eq_(len(res.authorities), len(self.authorities))
        eq_(len(res.additional), len(self.additional))
        
        resrest = res.answers + res.authorities + res.additional
        selfrest = self.answers + self.authorities + self.additional
        
        for (r,s) in zip(resrest, selfrest):
            eq_(r.name, s.name)
            eq_(r.qtype, s.qtype)
            eq_(r.qclass, s.qclass)
            eq_(r.ttl, s.ttl)
            eq_(r.rdlen, s.rdlen)
            eq_(r.rddata, s.rddata)

    def test_serialize(self):
        data = bytearray()
        prev = None
        a = dns.parser(self.buf)
        buf = a.serialize(data, prev)

        eq_(len(buf), len(self.buf))
        eq_(buf, self.buf)

#        fmt = arp._PACK_STR
#        res = struct.unpack(fmt, buf)
#
#        eq_(res[0], self.hwtype)
#        eq_(res[1], self.proto)
#        eq_(res[2], self.hlen)
#        eq_(res[3], self.plen)
#        eq_(res[4], self.opcode)
#        eq_(res[5], addrconv.mac.text_to_bin(self.src_mac))
#        eq_(res[6], addrconv.ipv4.text_to_bin(self.src_ip))
#        eq_(res[7], addrconv.mac.text_to_bin(self.dst_mac))
#        eq_(res[8], addrconv.ipv4.text_to_bin(self.dst_ip))
'''
    def _build_arp(self, vlan_enabled):
        if vlan_enabled is True:
            ethertype = ether.ETH_TYPE_8021Q
            v = vlan(1, 1, 3, ether.ETH_TYPE_ARP)
        else:
            ethertype = ether.ETH_TYPE_ARP
        e = ethernet(self.dst_mac, self.src_mac, ethertype)
        p = Packet()

        p.add_protocol(e)
        if vlan_enabled is True:
            p.add_protocol(v)
        p.add_protocol(self.a)
        p.serialize()
        return p

    def test_build_arp_vlan(self):
        p = self._build_arp(True)

        e = self.find_protocol(p, "ethernet")
        ok_(e)
        eq_(e.ethertype, ether.ETH_TYPE_8021Q)

        v = self.find_protocol(p, "vlan")
        ok_(v)
        eq_(v.ethertype, ether.ETH_TYPE_ARP)

        a = self.find_protocol(p, "arp")
        ok_(a)

        eq_(a.hwtype, self.hwtype)
        eq_(a.proto, self.proto)
        eq_(a.hlen, self.hlen)
        eq_(a.plen, self.plen)
        eq_(a.opcode, self.opcode)
        eq_(a.src_mac, self.src_mac)
        eq_(a.src_ip, self.src_ip)
        eq_(a.dst_mac, self.dst_mac)
        eq_(a.dst_ip, self.dst_ip)

    def test_build_arp_novlan(self):
        p = self._build_arp(False)

        e = self.find_protocol(p, "ethernet")
        ok_(e)
        eq_(e.ethertype, ether.ETH_TYPE_ARP)

        a = self.find_protocol(p, "arp")
        ok_(a)

        eq_(a.hwtype, self.hwtype)
        eq_(a.proto, self.proto)
        eq_(a.hlen, self.hlen)
        eq_(a.plen, self.plen)
        eq_(a.opcode, self.opcode)
        eq_(a.src_mac, self.src_mac)
        eq_(a.src_ip, self.src_ip)
        eq_(a.dst_mac, self.dst_mac)
        eq_(a.dst_ip, self.dst_ip)

    @raises(Exception)
    def test_malformed_arp(self):
        m_short_buf = self.buf[1:arp._MIN_LEN]
        arp.parser(m_short_buf)
'''
