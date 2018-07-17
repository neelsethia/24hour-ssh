import os
import sys
from pkg_resources import resource_filename

import boto3 
import json
#import pytest
import moto 
from moto import mock_ec2, mock_ssm

from ec2ssh import ssm

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

def test_build_send_command_document():
    pubkey_file = get_fixture_file('id_rsa.pub')
    pubkey = ssm.read_public_key_from_file(pubkey_file)
    response = ssm.build_send_command_document(pubkey)
    #print(response)
    assert isinstance(response, str)
    d = json.loads(response)
    assert isinstance(d, dict)
    assert d.get('schemaVersion') == '2.2'
    #assert False



param_name = 'secret'
param_value = 'that crazy little thing you do'
@mock_ssm
def test_set_encrypted_param():
    response = ssm.set_encrypted_param(param_name, param_value)
    assert isinstance(response['Version'], int)
    response = ssm.get_encrypted_param(param_name)
    assert response['Parameter']['Value'] == param_value




