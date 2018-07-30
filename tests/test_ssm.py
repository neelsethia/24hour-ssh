import os
import sys
from pkg_resources import resource_filename

import boto3 
import json
#import pytest
import moto 
from moto import mock_ec2, mock_ssm
import hashlib

from ec2ssh import ssm
from ec2ssh import prompter

def get_fixture_file(fixture_file):
    """Returns  path to named fixture file."""
    fixtures_dir = resource_filename(__name__, 'fixtures')
    fixture_file = os.path.join(fixtures_dir, fixture_file)
    return fixture_file


def test_read_public_key():
    pubkey_file = get_fixture_file('id_rsa.pub')
    assert os.path.exists(pubkey_file)
    response = ssm.read_public_key_from_file(pubkey_file)
    #print(response)
    assert isinstance(response, str)
    #assert False


def test_build_document():
    pubkey_file = get_fixture_file('id_rsa.pub')
    pubkey = ssm.read_public_key_from_file(pubkey_file)
    response = ssm.build_document(pubkey)
    #print(response)
    assert isinstance(response, str)
    d = json.loads(response)
    assert isinstance(d, dict)
    assert d.get('schemaVersion') == '2.2'
    #assert False


@mock_ssm
def test_upload_document():
    pubkey_file = get_fixture_file('id_rsa.pub')
    pubkey = ssm.read_public_key_from_file(pubkey_file)
    document = ssm.build_document(pubkey)
    document_name = 'sshPubkeySetup'
    client = ssm.get_ssm_client()
    ssm.upload_document(client, document_name,  document)
    response = client.describe_document(Name=document_name)
    print(response)
    sha256_hash = response['Document']['Hash']
    assert sha256_hash == hashlib.sha256(document.encode()).hexdigest()
    #assert False


AMI_IMAGE = 'ami-4e700e36'  #this is for US-WEST-2 ebs-ssd


@mock_ec2
def test_is_24hourssh_enabled():
    ec2 = boto3.resource('ec2',region_name='us-west-2' )
    test_instances = ec2.create_instances(ImageId=AMI_IMAGE, MinCount=2, MaxCount=2)
    test_instances[0].create_tags(Tags=[{ 'Key': '24hourssh', 'Value': 'enabled' }])
    assert prompter.is_24hourssh_enabled(test_instances[0])
    assert not prompter.is_24hourssh_enabled(test_instances[1])
    #assert False


@mock_ec2
def test_get_24hourssh_enabled_instances():
    ec2 = boto3.resource('ec2',region_name='us-west-2' )
    test_instances = ec2.create_instances(ImageId=AMI_IMAGE, MinCount=2, MaxCount=2)
    test_instances[0].create_tags(Tags=[{ 'Key': '24hourssh', 'Value': 'enabled' }])
    enabled = prompter.get_24hourssh_enabled_instances()
    print(enabled)
    assert enabled[0] == test_instances[0]
    #assert False


@mock_ec2
@mock_ssm
def test_send_command():
    ec2 = boto3.resource('ec2',region_name='us-west-2' )
    test_instances = ec2.create_instances(ImageId=AMI_IMAGE, MinCount=2, MaxCount=2)
    test_instances[0].create_tags(Tags=[{ 'Key': '24hourssh', 'Value': 'enabled' }])
    enabled = prompter.get_24hourssh_enabled_instances()

    document_name = 'sshPubkeySetup'
    pubkey_file = get_fixture_file('id_rsa.pub')
    pubkey = ssm.read_public_key_from_file(pubkey_file)
    document = ssm.build_document(pubkey)
    client = ssm.get_ssm_client()
    ssm.upload_document(client, document_name, document)

    response = ssm.send_command(client, enabled[0].id)
    print(response)
    assert response['Command']['DocumentName'] == document_name
    assert response['Command']['Status'] == 'Success'
    assert response['Command']['InstanceIds'][0] == enabled[0].id 
    #assert False

