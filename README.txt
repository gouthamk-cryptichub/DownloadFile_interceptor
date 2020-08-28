#Required pyhton Modules
netfilterqueue
scapy
optparse
argparse(for python 3)


**NOTE
If using this tool on a remote machine in the same network...
1) use ARP_spoofer to become man in the middle > https://github.com/gouthamk-cryptichub/ARP_spoofer
2) Set iptables rules in your machine as follows
    Open Terminal
    >iptables -I FORWARD -j NFQUEUE --queue-num 0
now use the tool

AFTER Experimen
Open Terminal
>iptables --flush