#!/bin/env python 
import sys 
import boto3 
import botocore
from botocore.exceptions import ClientError
import string 
import moto 
from moto import mock_ec2

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
    for instance in ec2.instances.all():
        print (instance.id, instance.state) 
        
def terminate_instances():
    instanceTerm = ec2.Instance(tempID)
    response = instanceTerm.terminate() 
    print (response)

#tests using moto from here
@mock_ec2
def test_new_instance():
    make_instance()
    client = boto3.client('ec2',region_name='us-west-2')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    assert len(instances) == 1
    instance1 = instances[0]
    assert instance1['ImageId'] == 'ami-4e700e36'
       
if __name__ == '__main__':
    #make_instance()
    test_new_instance()
    #list_instances()
    #print('=============')
    #terminate_instances()
    #print('=============')
    #list_instances()
    
    


