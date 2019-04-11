# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:30:35 2019

@author: Dell
"""
import hashlib 
import sys
from itertools import product

L = {}
counter = 0
found = 0
passwords_hashes = None
salts = []

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
    #if (counter%1000000 == 0):
    #print("{}: {}".format(counter,p_))
    #pass
        
def checkValidPass(password):
    string_ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    pass_string = [char for char in password if char not in string_ ]
    if(len(pass_string)>0):
        return False
    else:
        return True
    


def save_data(dict_name):
    global L 
    # Copy the results to a file
    output = open("output2c.txt".format(dict_name), "a+")
    output_text = ",".join(L.values())+','
    print("{}".format(output_text), file=output)
    output.close()
    

def load_dict():
    
    with open('C:/Users/Dell/Documents/courses/2019/semA/ISP/hw3/rockyou.txt','rb') as f:
        count =0
        inner_counter = 0;
        size_smaller = int(14344392/4)
        
        outer_counter = 0;
        current_file = open('dict_{}.txt'.format(0),"a+",encoding='utf-8')
                
        while(True):
            
            count+=1;
            inner_counter += 1
            if(inner_counter>size_smaller):
                outer_counter += 1;
                inner_counter = 0;
                if(current_file):
                    current_file.close()
                current_file = open('dict_{}.txt'.format(outer_counter),"a+",encoding='utf-8')
                
            line = f.readline()
            if(not line):    
                current_file.close()                
                break
            try:
                decoded = line.decode('utf8')
                decoded = decoded.strip()
                if(checkValidPass(decoded)):
                    current_file.write("{}\n".format(decoded))
            except:
                pass
            
    
    print(count)
    

def load_sub_dict(dict_path,is_full_path = False):
    string_ = 'ABCDEF0123456789'
    if(not is_full_path):
        dict_path = 'C:/Users/Dell/Documents/courses/2019/semA/ISP/hw3/{}'.format(dict_path)
    with open(dict_path,encoding='utf-8') as f:

        while(True):
                
            line = f.readline()
            
            word = line.strip()
            
            for s in salts:
                check_password(word + ''.join(s))

            if(not line):                   
                break
    
    save_data(dict_path.split('/')[-1].split('.')[0])

   
def load_hashes():
    global passwords_hashes,salts
    with open('C:/Users/Dell/Documents/courses/2019/semA/ISP/hw3/hw3_ex2.txt') as f:
        count =0
        hashes = []
        while(True):
            
            count+=1;
            
            line = f.readline()
            if(not line):
                break
            if(count >=24 and count <= 33):
                salt,hash_ = line.split(',')
                hashes.append(hash_.strip())
                salts.append(salt.strip())
            elif count>33:
                print('next line not hash')
                print(line)
                break
    
    passwords_hashes = [x.strip() for x in hashes]   
    return passwords_hashes

if __name__ == '__main__':
    dict_path = sys.argv[1]
    dict_path = 'dict_'+dict_path+'.txt'
    #load_dict()
    load_hashes()
    load_sub_dict(dict_path)
    
    