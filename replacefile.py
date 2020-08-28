#!/usr/bin/env python
import netfilterqueue as netq
import scapy.all as scapy

def mod_packet(packet):
    use_packet = scapy.IP(packet.get_payload())
    if use_packet.haslayer(scapy.Raw):
        if use_packet[scapy.TCP].dport == 80:
            print("[+] HTTP Request...")
            print(use_packet.show())
        if use_packet[scapy.TCP].sport == 80:
            print("[+] HTTP Response...")
            print(use_packet.show())
    packet.accept()

queue = netq.NetfilterQueue()
queue.bind(0, mod_packet)
queue.run()