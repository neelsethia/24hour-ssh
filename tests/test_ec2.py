#!/bin/env python 
import sys 
import boto3 
import botocore
from botocore.exceptions import ClientError
import string 
import moto 

ec2 = boto3.resource('ec2')

def make_instance():
    instance = ec2.create_instances(
        ImageId='ami-4e700e36', #this is for US-WEST-2 ebs-ssd
        MinCount=1,
        MaxCount=1,
        InstanceType='t1.micro' #t1.micro only works with EBS-SSD 
        )
    global tempID
    tempID = instance[0].id 

def list_instances():
    
    


