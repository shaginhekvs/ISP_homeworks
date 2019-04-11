from netfilterqueue import NetfilterQueue
import time
import json
import pickle
from datetime import datetime

from scapy.all import *
def print_and_accept(pkt):

    ip = IP(pkt.get_payload())
    if(ip.haslayer(Raw)):
    	http = ip[Raw].load.decode()
    	print(http)
    	try:
    		json.loads(http)
    	except Exception as e:
    		print (e)
    		path = 'shared/'
    		pickle.dump(http,open(path+'http '+str(datetime.utcnow()),'wb'))
    if(ip.haslayer(TCP)):
    	#print(str(ip[TCP].payload))
    	#print(str(ip[IP].dst))
    	#print(str(ip[TCP].dport))
    	pass
    #print(pkt.get_payload())
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept,100)

try:
	nfqueue.run();
except Exception as e:
	print(e)

time.sleep(10)
nfqueue.unbind()

