import asyncio
import websockets
import binascii
from random import randint
import hashlib

N="EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
N_int = int(N,16)
g = 2
def genA(a):
	A = pow(g,a,N_int)
	A_b, _ = encodeInt(A)
	return A_b , A

def genRandInt(num_digits = 32):
	s = ""
	for i in range(num_digits):
		s += str(randint(0, 9))
	if(len(s)>0):
		return int(s)
	else:
		return randint(0,9)
def decodeIntMsg(msgReceived):
	buff = binascii.unhexlify(msgReceived)
	return buff , int.from_bytes(buff,'big')

def encodeInt(i):
	buff = i.to_bytes((i.bit_length()+7)//8,'big')
	return buff , binascii.hexlify(buff).decode('utf-8')

def finalHash(A_b,B_b,S_b):
	hash_ = hashlib.sha256()
	hash_.update(A_b)
	hash_.update(B_b)
	hash_.update(S_b)
	return int(hash_.hexdigest(),16)
def getS(a,A_b,salt_b,B,B_b):
	mypass = "JQAFDRNWXRYHCkcJYA0FCw1AQxw="
	U = "keshav.singh@epfl.ch"
	hashU = hashlib.sha256();
	hashU.update(A_b)
	hashU.update(B_b)
	u = int(hashU.hexdigest(), 16)
	hashInner = hashlib.sha256();
	hashInner.update(U.encode('utf-8'));
	hashInner.update(":".encode('utf-8'));
	hashInner.update(mypass.encode('utf-8'));
	x1 = hashInner.digest()
	hashOuter = hashlib.sha256();
	hashOuter.update(salt_b)
	hashOuter.update(x1)
	x = int(hashOuter.hexdigest(),16)
	S = pow(B - pow(g,x,N_int),a+u*x,N_int)
	return S


async def hello():
    async with websockets.connect(
            'ws://com402.epfl.ch/hw2/ws') as websocket:
        #name = input("What's your name? ")
        email_ = "keshav.singh@epfl.ch"
        #send email
        await websocket.send(email_.encode('utf-8'))
        print(f"> {email_}")

        greeting = await websocket.recv()
        print(f"< {decodeIntMsg(greeting)}")
        salt_b,salt = decodeIntMsg(greeting)
        print('sending A')
        a = genRandInt()
        A_b,A = genA(a)
        
        #send A
        A_b,A_s= encodeInt(A)
        await websocket.send(A_s)
        
        #get B
        b_str = await websocket.recv()
        print('got B')
        B_b, B =decodeIntMsg(b_str)
        print(f"< {B}")
        S = getS(a,A_b,salt_b,B,B_b)
        print(f"< {S}")
        S_b,S_string = encodeInt(S)
        #send A||B||S
        out_b,out_string = encodeInt(finalHash(A_b,B_b,S_b))
        await websocket.send(out_string)
        
        # get token
        final_ = await websocket.recv()

        print(f"> {final_}")


asyncio.get_event_loop().run_until_complete(hello())