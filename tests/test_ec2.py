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
        
def terminate_instances(termID):
    instanceTerm = ec2.Instance(termID)
    response = instanceTerm.terminate() 
    #print (response)


#tests using moto from here


#tests making an ec2 instance with the make_instance function
@mock_ec2
def test_new_instance():
    make_instance()
    client = boto3.client('ec2',region_name='us-west-2')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    assert len(instances) == 1
    instance1 = instances[0]
    assert instance1['ImageId'] == 'ami-4e700e36'


#tests whether an instance is terminated after calling terminate_instances
@mock_ec2
def test_delete_instance():
   tempec2 = boto3.resource('ec2')
   make_instance()
   terminate_instances(tempID)
   for instance1 in tempec2.instances.all(): 
        if tempID is instance1.id:
            print ('reached')
            assert instance.state == 'terminated' or 'shutting-down'

if __name__ == '__main__':
    #make_instance()
    test_new_instance()
    test_delete_instance()
    #list_instances()
    #print('=============')
    #terminate_instances()
    #print('=============')
    #list_instances()
    
    

