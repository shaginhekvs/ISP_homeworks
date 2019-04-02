import requests
import json 
import base64
mySecureOneTimePad = "Never send a human to do a machine's job";
def superencryption(msg,key):
	if(len(key)<len(msg)):
		diff = len(msg)-len(key)
		key += key[0:diff];
	print(len(msg))
	amsg = [ord(a) for a in msg]
	key_sub = key[0:len(msg)]
	akey = [ord(a) for a in key_sub]
	res = []
	for a,b in zip(amsg,akey):
		res.append(chr(a^b))
	res2 = base64.b64encode("".join(res).encode())
	return "".join(chr(c) for c in res2)

print(superencryption("keshav.singh@epfl.ch",mySecureOneTimePad))
mypass = "JQAFDRNWXRYHCkcJYA0FCw1AQxw="


r = requests.post('http://127.0.0.1:5000/hw2/ex1', json = {'pass':'PgQFFgVPAQE='})

print(r.text)
print(r.status_code)