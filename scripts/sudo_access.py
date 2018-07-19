#!/bin/env python 

#Script which will prompt for username, target host, and the reason for access request. 
#Script will generate temporary ssh keypair. 
#Script will call ssm service to install generated ssh public key into described file. 
#Script will delete temporary ssh keypair from cloud9 instance after 24 hours.  

import subprocess
import sys 
import string 
import os 
import boto3
import botocore
from botocore.exceptions import ClientError
import moto 
import datetime
from os import chmod 
from Crypto.PublicKey import RSA 
import paramiko


def target_prompt():
    global targetHost
    targetHost = input("What is the desired target host?")
    
    #test whether target host is valid
    
    
    ec2 = boto3.resource('ec2')
    
    
    
    #then do what
 
#def list_all_resources():

   
#def pull_local_instance(): 
    #this will be for determining the local c9 instance
        #user is running

def generate_key_paramiko(filename, passwd):
    cwd = os.getcwd()
    key = paramiko.RSAKey.generate(1024)
    key.write_private_key_file(filename,passwd)
    chmod(filename, 600)
    
    cwd = os.getcwd()
    out = open(cwd +'/pkey.pub', 'w').write(key.get_base64())
        
def generate_key_crypto(): 

#this will generate ssh keypair 
      
    key = RSA.generate(2048)
    cwd = os.getcwd()
    with open(cwd + "/private.key", 'wb') as content_file: 
        chmod(cwd + "/private.key", 600)
        content_file.write(key.exportKey('PEM'))
    pubkey = key.publickey()
    with open(cwd + "/public.key", 'w') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))
    


#def transfer_key(): 
    #use SSM to transfer public key to target instance 
    
    

#def log_user_input():
        


if __name__ == '__main__':
