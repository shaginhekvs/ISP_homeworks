Ex1 solution : 
1. Inspect the login page http://com402.epfl.ch/hw1/ex1 and see the script. In the script one can see that the variable enc :  var enc = superencryption(username,mySecureOneTimePad) must be equal to password to successfully login. 
2. Get the value generated by superencryption and then enter the same in the password field for successful login. 

Ex2 Solution : 
http://com402.epfl.ch/hw1/ex2/login tracks people. This is the clue that they would have a cookie !! Maybe cookie gives some hints on how to proceed. The cookie is "a2VzaGF2LnNpbmdoQGVwZmwuY2gsMTU1MjQyOTg2Nixjb200MDIsaHcxLGV4MSx1c2Vy" in base64, changing it to UTF-8 gives : keshav.singh@epfl.ch,1552429866,com402,hw1,ex1,user : so one of this value should be the one we could change to get past security. Most likely it is user which should be changed to admin . I tried with admin and it failed, and with administrator and changing the LoginCookie of the application to : "a2VzaGF2LnNpbmdoQGVwZmwuY2gsMTU1MjQyOTg2Nixjb200MDIsaHcxLGV4MSxhZG1pbmlzdHJhdG9y" made the login attempt as superuser successful. 

Ex3 solution : 
As can be seen in interceptor script, I parsed the payload of the packet and save the packets as a pickle which have HTTP content in them into the shared folder so that I can use them later. 
a. Sending Traffic : In parser_http.py file, we can see in def parser(file)  function, when the packet is type , I get the payload and then change the shipping address to keshav.singh@epfl.ch and create a new request with same headers as that of the packet we captures , with the new shipping_address and send the POST request to : http://com402.epfl.ch/hw1/ex3/shipping

Ex4 Solution : 
We used the same packets which were saved by interceptor.py and write scripts to capture the CC info and passwords in parser_http.py . Function parser(file) checks first if there is a CC info in the packet by invoking function check_cc which checks if the packet is transaction type and contains CC in the text and --- , then it finds 4 groups of 4 digits separated by delimiter if it can and result is returned back. Next parser(file) looks for pwd in the function by checking if pwd and --- in the packet then checking if the string after -- is a valid password by invoking isValidPwd(pwd) which returns true if the password length is valid and the characters in the password are all allowed characters. All the 5 secrets are checked for duplicity and saved. ex4.py then sends them to "http://com402.epfl.ch/hw1/ex4/sensitive" by POST request , after adding requisite headers and data. 





