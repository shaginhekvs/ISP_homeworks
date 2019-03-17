import requests
import json

if __name__=='__main__':
	secrets = ['6343/7920/7804/5771', '4755/2380/4931/5945', '9855.5488.4007.5276','VUXBR=EDP81Q=', '<H=<NF?3KA12OA']
	headers = { 'User-Agent': 'Dumb Generator', 'Content-Type': 'application/json'}
	data= {'student_email':'keshav.singh@epfl.ch','secrets':secrets}
	res = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", headers = headers,data=json.dumps(data))
	print(res.status_code)
	print(res.reason)
	print(res.text)

