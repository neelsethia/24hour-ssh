#!/bin/env python 
"""
Explore boto3 ssm client
"""

import boto3 
import moto 
from moto import mock_ec2, mock_ssm
import test_ec2

def ssm_list_instance_tags(instance_id):
    ssm = boto3.client('ssm')
    response = ssm.list_tags_for_resource(
        ResourceType='ManagedInstance',
        ResourceId=instance_id,
    )
    return response['TagList']

def ssm_add_instance_tags(instance_id, tags):
    ssm = boto3.client('ssm')
    ssm.add_tags_to_resource(
        ResourceType='ManagedInstance',
        ResourceId=instance_id,
        Tags=tags,
    )

def ssm_send_command(instance_id, command_doc_name):
    ssm = boto3.client('ssm')
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName=command_doc_name,
        TimeoutSeconds= 3600,
        Parameters=dict(),
    )
    return response

def ssm_set_encrypted_param(param_name, param_value, key_id=None):
    ssm = boto3.client('ssm')
    kwargs = dict(
        Name=param_name,
        Value=param_value,
        Type='SecureString',
        Overwrite=True,
    )
    if key_id:
        kwargs['KeyId'] = key_id
    response = ssm.put_parameter(**kwargs)
    return response['Version']

def ssm_get_encrypted_param(param_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=param_name,
        WithDecryption=True,
    )
    return response

def ssm_set_list_param(param_name, param_value_list):
    ssm = boto3.client('ssm')
    value = ','.join(param_value_list)
    response = ssm.put_parameter(
        Name=param_name,
        Value=','.join(param_value_list),
        Type='StringList',
        Overwrite=True,
    )
    return response

def ssm_get_param(param_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=param_name,
    )
    return response



param_name = 'passwd'
param_value = 'doiu*(.3szjk'

@mock_ssm
def test_ssm_set_param():
    response = ssm_set_encrypted_param(param_name, param_value)
    print(response)
    assert isinstance(response, int)

@mock_ssm
def test_ssm_get_param():
    ssm_set_encrypted_param(param_name, param_value)
    response = ssm_get_encrypted_param(param_name)
    print(response)
    assert response['Parameter']['Value'] == param_value


param_name = 'MyStruggle'
param_value_list = [
    'today I suffer',
    'under extreem duress',
    'the ineptitude of my peers',
    'chmod 777 for crying out loud',
]
@mock_ssm
def test_ssm_list_param():
    ssm_set_list_param(param_name, param_value_list)
    response = ssm_get_param(param_name)
    print(response['Parameter']['Value'])
    assert response['Parameter']['Value'] == param_value_list.split(',')



@mock_ec2
@mock_ssm
def test_ssm_list_instance_tags():
    instance_id = test_ec2.make_instance()
    tags=[
        { 'Key': 'team', 'Value': 'seg' },
        { 'Key': 'app', 'Value': '24hour-ssh' },
        { 'Key': 'env', 'Value': 'test' },
    ]
    ssm_add_instance_tags(instance_id, tags)
    tags_found = ssm_list_instance_tags(instance_id)
    assert tags_found == tags


@mock_ec2
@mock_ssm
def test_ssm_send_command():
    instance_id = test_ec2.make_instance()
    command_doc_name = 'AWS-RestartEC2Instance'
    response = ssm_send_command(instance_id, command_doc_name)
    assert response['Command']['Status'] in ['Pending','InProgress','Success','Cancelled','Failed','TimedOut','Cancelling']
