from flask import Flask, abort, request
import json 
import base64
app = Flask(__name__)

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

@app.route("/hw2/ex1",methods=['GET', 'POST'])
def hello_world():
	print(request.get_json())
	bad = json.dumps({'success':False}), 400, {'ContentType':'application/json'} 
	if not request.json:
		return bad
	print (request.json)
	json_ = request.json
	if('user' not in json_.keys() or 'pass' not in json_.keys()):
		return bad
	if((len(json_['user'])>100) or len(json_['pass'])>100):
		return bad
	if( superencryption(json_['user'],mySecureOneTimePad) != json_['pass'] ):
		return bad
	print('passed')
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


if __name__ == '__main__':
	app.run(host = "127.0.0.1",port = 5000)