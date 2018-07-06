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
import datetime
from os import chmod 
from Crypto.PublicKey import RSA 




def userPrompt:
  

def targetPrompt:
    global targetHost
    targetHost = input("What is the desired target host?")
    
    #test whether target host is valid
    
    
    ec2 = boto3.resource('ec2')
    
    #then do what
    
    
        
def generateKey: 
    #this will generate ssh keypair 
    key = RSA.generate(2048)
    #with open("/tmp/private.key", 'w') as content_file:
    #    chmod("/temp/private.key", 0600)
     #   content_file.write(key.exportKey('PEM'))
    global pubkey
    pubkey = key.publickey()
    with open("/tmp/public.key",'w') as content_file:
        content_file.write(public.exportKey('OpenSSH'))


def transferKey: 
    #use SSM to transfer public key to target instance 
    

def logUserInput:
        
        