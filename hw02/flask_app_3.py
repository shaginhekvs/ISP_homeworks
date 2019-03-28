import flask 
from flask import Flask, request, abort, Response ,make_response, render_template
import json
import base64
import hmac

app = Flask(__name__)

# My secret key from HW1
secret_key = 'KAoDBBYOHgQUAU4hRRgTAU8NSA=='

#@app.route('/')
#def index():
 #   return render_template('index.html')

# Message that is required to be displayed when decoding the cookie for administrator
message_cookie_admin = ','.join(['administrator','42','com402','hw2','ex3','administrator'])

# Calculating the hmac value of the administrator cookie
# Global because this won't be changing, since we have a fixed username and password
hmac_administrator = hmac.new(key= secret_key.encode('utf8'), msg=message_cookie_admin.encode())
hmac_administrator_value = hmac_administrator.hexdigest()

@app.route('/ex3/login', methods = ['POST', 'GET'])
def setcookie():

    # Waiting for a post request
    if request.method == 'POST':

        # Extracting dat from the json file
        data = request.get_json()

        # Fetch username and password
        user = data['user']
        password = data['pass']

        #Create a responspe object
        resp = make_response()

        #Checking the username and password to give the appropriate cookie
        if (user == 'administrator') and (password == '42'):

            cookie_and_hmac_admin = message_cookie_admin + ',' + hmac_administrator_value
            # Encode the cookie using base64
            cookie_value= base64.b64encode(cookie_and_hmac_admin.encode()).decode()

            # Setting the cookie value and name
            resp.set_cookie('LoginCookie', cookie_value)

            # Returning the cookie and status code 200 for administrator
            return resp, 200
        else:

            # If the username and password aren't as above, then it is a normal user
            type_user = 'user'
            # Set the message of the cookie
            message_cookie_user = ','.join([user,password,'com402','hw2','ex3',type_user])
            # Create the hmac object and value for the user
            hmac_user = hmac.new(key= secret_key.encode('utf8'), msg=message_cookie_user.encode())
            cookie_and_hmac_user = message_cookie_user + ',' + hmac_user.hexdigest()
            # Encode the cookie using base 64
            cookie_value= base64.b64encode(cookie_and_hmac_user.encode()).decode()
            # Setting the cookie value and name
            resp.set_cookie('LoginCookie', cookie_value)

            #Returning he cookie and status code 201 for user
            return resp, 201


@app.route('/ex3/list',methods=['GET','POST'])
def check_tampering():

    # Upon a none Post request, we can fetch the data previously recorded by the cookie
    name = request.cookies.get('LoginCookie')

    # Decoding the base64 encoding
    decoded_cookie_value = base64.b64decode(name).decode()

    # Fetching the hmac value, that occurs at the end of the string
    hmac_value = decoded_cookie_value.split(',')[-1]
    # Fetching the rest of the daata to compute the hmac, to see if it has been tampered
    message = ','.join(decoded_cookie_value.split(',')[0:-1])

    # Fetching the username
    user = decoded_cookie_value.split(',')[0]
    # Fetching the password
    password = decoded_cookie_value.split(',')[1]

    # Calculating the hmac from the message we have given the secret key
    hmac_code = hmac.new(key= secret_key.encode('utf8'), msg=message.encode()).hexdigest()

    # Checking the if the hmac_value from the cookie matches the hmac_administrator_value, and the computed hmac_code (to check for tampering)
    if (hmac_code == hmac_value == hmac_administrator_value):

        return '', 200

    else:
        
        # Checking if it isn't an administrator but, the hmac_code and hmac_value matches, which implies no tampering and a "user"
        if hmac_code == hmac_value:

            return '', 201
        # Tampering with the cookie
        else:

            return abort(403)

        

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=5000 ,debug=True)