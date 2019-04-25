#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

## This method returns a list of messages in a json format such as 
## [
##  { "name": <name>, "message": <message> },
##  { "name": <name>, "message": <message> },
##  ...
## ]
## If this is a POST request and there is a parameter "name" given, then only
## messages of the given name should be returned.
## If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages",methods=["GET","POST"])
def messages():

    # List output
    result = []
    with db.cursor() as cursor:
        # Checking if the request is a POST
        if request.method == 'POST':
            # Fetching the name
            name = request.form['name']
            # Checking if the field is empty or None
            if name is None:
                return jsonify([{}]), 500

            # Executing query
            cursor.execute("SELECT * FROM messages WHERE name=%s", name)
            # Fetching results
            json_file = list(cursor.fetchall())
            # Appending results in array
            for item in json_file:
                result.append({"name": item[0], "message": item[1]})

            # Return values
            return jsonify(result), 200

        # Checking if the request is a GET
        if request.method == 'GET':
            # Executing query
            cursor.execute("SELECT * FROM messages")
            # Fetching results
            json_file = list(cursor.fetchall())
            # Appending results in array
            for item in json_file:
                result.append({"name": item[0], "message": item[1]})
            # Return values
            return jsonify(result) , 200

## This method returns the list of users in a json format such as
## { "users": [ <user1>, <user2>, ... ] }
## This methods should limit the number of users if a GET URL parameter is given
## named limit. For example, /users?limit=4 should only return the first four
## users.
## If the paramer given is invalid, then the response code must be 500.
@app.route("/users",methods=["GET"])
def contact():

    # Dictionary output
    result = {}

    with db.cursor() as cursor:
        # Fetching the limit in the get request
        limit = request.args.get('limit')

        # Checking if the input is a string that can be converted to a number 
        # or a None or a string that contains malicious input
        try:
            limit = int(limit)

        except ValueError:

            # Malicious input
            return "", 500

        except TypeError:
            # Checking if the limit is none, and returning all the users
            if limit is None:
                
                cursor.execute("SELECT name FROM users")
                json_file = list(cursor.fetchall())
                result["users"] = [item[0] for item in json_file]

                return jsonify(result),200

        # If the number is a negative number return 500
        if limit < 0:
            
            return "", 500
        
        # If it's equal to zero, return empty dictionary
        elif limit == 0:
            return jsonify({"users": []}), 200

        # If limit is a number that can actually be passed to the query
        else:
            cursor.execute("SELECT name FROM users limit %s", limit)
            json_file = list(cursor.fetchall())
            result["users"] = [item[0] for item in json_file]

            return jsonify(result),200

if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]
    
    db = pymysql.connect("localhost",
                username,
                password,
                database)
    with db.cursor() as cursor:
        populate.populate_db(seed,cursor)             
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0',port=80)
