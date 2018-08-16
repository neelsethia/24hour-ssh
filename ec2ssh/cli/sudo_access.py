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
    return targetHost
        
    
def transfer_key(target): 
    #use SSM to transfer public key to target instance
    pub_key = ssm.read_public_key_from_file("pkey.pub")
    print(pub_key)
    client = ssm.get_ssm_client()
    document = ssm.build_document(pub_key)
    
    #configure ssm on target instance
        #perhaps need to modify the instance through some CF mods 
    
    
    #call ssm send command from here to designated instance 
    ssm.upload_document(client, "sshPubkeySetup", document)
    ssm.send_command(client, target)
    
    
    
    

#generating an SSH keypair
def generate_key_paramiko(filename, passwd):
    cwd = os.getcwd()
    key = paramiko.RSAKey.generate(1024)
    key.write_private_key_file(filename,passwd)
    chmod(filename, 600)
    
    cwd = os.getcwd()
    out = open(cwd +'/pkey.pub', 'w').write(key.get_base64())



    
if __name__ == "__main__":
    #generate_key_paramiko("private.key", "hello")
    targetHost = target_prompt_selector()
    #transfer_key(targetHost)
