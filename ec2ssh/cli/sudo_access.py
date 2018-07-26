#!/bin/env python 

#Script which will prompt for username, target host, and the reason for access request. 
#Script will generate temporary ssh keypair. 
#Script will call ssm service to install generated ssh public key into described file. 
#Script will delete temporary ssh keypair from cloud9 instance after 24 hours.  
import os
import subprocess
import sys 
from ec2ssh import ssm 
from ec2ssh import prompter
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
        #lists all instances with the key and tag for 24hourssh and enabled 
    #print(get_24hourssh_enabled_instances())
    print("======================")
    prompter.test_output()
    print("======================\n")
    
    #user enters desired target host
    while True:
        targetHost = input("What is the desired target host? (Enter the Instance ID): ")
        targetHost = str.strip(targetHost)
        #check that entered ID matches with the ID's given in get_24hourssh_enabled_instances 
        if not prompter.compare_24hourssh_enabled_instance_ID(targetHost):
            print("The instance ID you have entered is invalid!")
            continue
        else:
            break
    transfer_key(targetHost)
        
    
def transfer_key(target): 
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
