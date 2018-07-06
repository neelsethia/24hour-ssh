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
