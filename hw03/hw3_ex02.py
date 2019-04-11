# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:45:47 2019

@author: Dell
"""

import pickle
from itertools import product
import hashlib

L = {}
counter = 0
found = 0
passwords_hashes = None

def check_password(password):
    global passwords_hashes,L,counter,found
    p_ = password
    password_hash = hashlib.sha256(p_.encode()).hexdigest()
    
    for pwd in passwords_hashes:
        if(pwd == password_hash) and (pwd not in L):
            print('found: {} with hash {}'.format(p_,pwd) )
            found += 1
            L[pwd] = p_
    counter += 1
    if (counter%1000000 == 0):
        print("{}: {}".format(counter,p_))
        


def save_data():
    global L 
    # Copy the results to a file
    output = open("output.txt", "w")
    output_text = "\n".join(L.values())
    print("{}".format(output_text), file=output)
    output.close()
    
    
def load_hashes():
    global passwords_hashes
    with open('C:/Users/Dell/Documents/courses/2019/semA/ISP/hw3/hw3_ex2.txt') as f:
        count =0
        hashes = []
        while(True):
            
            count+=1;
            
            line = f.readline()
            if(not line):
                break
            if(count >=2 and count <= 11):
                hashes.append(line)
            elif count>11:
                print('next line not hash')
                print(line)
                break
    
    passwords_hashes = [x.strip() for x in hashes]   
    return passwords_hashes

        

if __name__ == '__main__':
    load_hashes()
    string_ = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(4,7):
        for s in product(string_,repeat = i ):
            check_password(''.join(s))
            if(found>=len(passwords_hashes)):
                break
    save_data()
        


                    
