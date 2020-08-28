#!/usr/bin/env python
import netfilterqueue as netq
import scapy.all as scapy

def mod_packet(packet):
    use_packet = scapy.IP(packet.get_payload())
    packet.set_payload(str(use_packet))
    packet.accept()

queue = netq.NetfilterQueue()
queue.bind(0, mod_packet)
queue.run()