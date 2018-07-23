import boto3 
import moto 
from moto import mock_ec2, mock_ssm
import test_ec2

from ec2ssh.samples import ssm


param_name = 'passwd'
param_value = 'doiu*(.3szjk'

@mock_ssm
def test_ssm_set_param():
    response = ssm.ssm_set_encrypted_param(param_name, param_value)
    print(response)
    assert isinstance(response, int)

@mock_ssm
def test_ssm_get_param():
    ssm.ssm_set_encrypted_param(param_name, param_value)
    response = ssm.ssm_get_encrypted_param(param_name)
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
    ssm.ssm_set_list_param(param_name, param_value_list)
    response = ssm.ssm_get_param(param_name)
    print(response['Parameter']['Value'])
    assert response['Parameter']['Value'] == (',').join(param_value_list)



@mock_ec2
@mock_ssm
def test_ssm_list_instance_tags():
    instance_id = test_ec2.make_instance()
    tags=[
        { 'Key': 'team', 'Value': 'seg' },
        { 'Key': 'app', 'Value': '24hour-ssh' },
        { 'Key': 'env', 'Value': 'test' },
    ]
    ssm.ssm_add_instance_tags(instance_id, tags)
    tags_found = ssm.ssm_list_instance_tags(instance_id)
    assert tags_found == tags


@mock_ec2
@mock_ssm
def test_ssm_send_command():
    instance_id = test_ec2.make_instance()
    command_doc_name = 'AWS-RestartEC2Instance'
    response = ssm.ssm_send_command(instance_id, command_doc_name)
    assert response['Command']['Status'] in ['Pending','InProgress','Success','Cancelled','Failed','TimedOut','Cancelling']
