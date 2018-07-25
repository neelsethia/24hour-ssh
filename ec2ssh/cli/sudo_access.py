#!/bin/env python 

#Script which will prompt for username, target host, and the reason for access request. 
#Script will generate temporary ssh keypair. 
#Script will call ssm service to install generated ssh public key into described file. 
#Script will delete temporary ssh keypair from cloud9 instance after 24 hours.  

import subprocess
import sys 
import os.path 
sys.path.append(os.path.abspath(os.path.join('../..','ec2ssh')))
from ssm import get_24hourssh_enabled_instances
#try to import ec2ssh.ssm 
#import ec2ssh.ssm 
import string 
import boto3
import botocore
from botocore.exceptions import ClientError
import datetime
from os import chmod 
import moto
import paramiko



def target_prompt_selector():
    ec2 = boto3.resource('ec2')
    
    #function call to SSM (for now until modularize) to list instances with key, tag
    print(get_24hourssh_enabled_instances())
    
    
    
    #user enters desired target host
    global targetHost
    targetHost = input("What is the desired target host? (Enter the Instance ID):\n")
    targetHost = str.strip(targetHost)
    print(targetHost)
    
    

    
    
def transfer_key(): 
    #use SSM to transfer public key to target instance
    print("transfer_key function filler")

#generating an SSH keypair
def generate_key_paramiko(filename, passwd):
    cwd = os.getcwd()
    key = paramiko.RSAKey.generate(1024)
    key.write_private_key_file(filename,passwd)
    chmod(filename, 600)
    
    cwd = os.getcwd()
    out = open(cwd +'/pkey.pub', 'w').write(key.get_base64())


    
if __name__ == "__main__":
    target_prompt_selector()
