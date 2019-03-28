from flask import Flask, abort, request
import json 
import hmac
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

def generateBase64(msg):
	m = "".join([chr(c) for c in msg])
	return base64.b64encode(m)

def getHMAC(msg):
	hmac_ = hmac.new(my_pass)
	hmac_.update(msg_without_hash)
	hmac_this = hmac_.hexdigest()
	return hmac_this

def decodeBase64(msg):
	msg_decoded  = base64.b64decode(msg)
	msg_splitted = msg_decoded.split(',')
	if(len(msg_splitted) != 7 ):
		print('msg below doesnt conform')
		print(msg_decoded)
	msg_without_hash = ",".join(msg_splitted[:-1])
	print(msg_without_hash)
	hmac_this = getHMAC(msg_without_hash)
	print('2 hashes are :')
	print(msg_splitted[-1])
	print(hmac_this)
	if(hmac.compare_digest(hmac_this,msg_splitted[-1])):
		return True
	else:
		return False

def makeCookieString(username,password):
	userType = 'user'
	if(username == 'administrator' and password == '42'):
		userType = 'administrator'
	reply = username+','+str(millis = int(round(time.time() )))+',com402,hw2,ex3,'+userType
	hmac_this = getHMAC(reply)
	reply += ','+hmac_this
	return generateBase64(reply)

my_pass = superencryption("keshav.singh@epfl.ch",mySecureOneTimePad);

@app.route("/ex3/login",methods=['GET', 'POST'])
def hello_world():
	print(request.get_json())
	bad = json.dumps({'success':False}), 400, {'ContentType':'application/json'} 
	if not request.json:
		return bad
	print (request.json)
	json_ = request.json
	if('user' not in json_.keys() or 'pass' not in json_.keys()):
		return bad
	resp = flask.make_response()
	resp.set_cookie('LoginCookie', makeCookieString(json_['user'],json_['pass']))
	return resp

@app.route("/ex3/login",methods=['GET', 'POST'])
def hello_world2():
	print(request.get_json())
	cookie = request.cookies.get('LoginCookie')
	badFake = json.dumps({'success':False}), 403, {'ContentType':'application/json'} 
	goodUser = json.dumps({'success':False}), 201, {'ContentType':'application/json'} 
	goodAdmin = json.dumps({'success':False}), 200, {'ContentType':'application/json'} 
	res,userType = decodeBase64(cookie)
	if(res):
		if(userType=='user'):
			return goodUser
		else:
			return goodAdmin
	else:
		return badFake 


if __name__ == '__main__':
	app.run(host = "127.0.0.1",port = 5000)