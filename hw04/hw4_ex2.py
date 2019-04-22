# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 12:00:44 2019

@author: Dell
"""

import bcrypt
import flask
from flask import Flask, request, abort, Response ,make_response, render_template
import json



app = Flask(__name__)

@app.route('/hw4/ex2', methods = ['POST', 'GET'])
def ret_pass():

    # Extracting dat from the json file
    data = request.get_json()

    # Fetch username and password
    user = data['user']
    password = data['pass']
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8'),200



if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=5000 ,debug=True)