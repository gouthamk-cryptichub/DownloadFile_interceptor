#!/usr/bin/env python
import netfilterqueue as netq
import scapy.all as scapy

def mod_packet(packet):
    use_packet = scapy.IP(packet.get_payload())
    if use_packet.haslayer(scapy.Raw):
        if use_packet[scapy.TCP].dport == 80:
            print("[+] HTTP Request...##########")
            if ".exe" in use_packet[scapy.Raw].load:
                print("[+] Detected Download .exe file REQUEST...")
                print(use_packet.show())
        elif use_packet[scapy.TCP].sport == 80:
            print("[+] HTTP Response...#########")
            print(use_packet.show())
    packet.accept()

queue = netq.NetfilterQueue()
queue.bind(0, mod_packet)
queue.run()