import os
import boto3 
import yaml
import json

DEFAULT_PUBKEY='~/.ssh/id_rsa.pub'

def read_public_key_from_file(pubkey_file):
    with open(pubkey_file, 'r') as pubkey:
        return pubkey.read()


def send_command(instance_id, command_doc_name):
    ssm = boto3.client('ssm')
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName=command_doc_name,
        TimeoutSeconds= 3600,
        Parameters=dict(),
    )
    return response

def set_encrypted_param(param_name, param_value, key_id=None):
    ssm = boto3.client('ssm')
    kwargs = dict(
        Name=param_name,
        Value=param_value,
        Type='SecureString',
        Overwrite=True,
    )
    if key_id:
        kwargs['KeyId'] = key_id
    return ssm.put_parameter(**kwargs)

def get_encrypted_param(param_name):
    ssm = boto3.client('ssm')
    return ssm.get_parameter(
        Name=param_name,
        WithDecryption=True,
    )

def build_send_command_document(pubkey):
    document = dict(
        schemaVersion='2.2',
        description='Install ssh public key into ~ec2-user/.ssh/authorized_keys',
        parameters=dict(),
        mainSteps=[
            dict(
                action='aws:runShellScript',
                name='sshPubkeySetup',
                inputs=dict(
                    runCommandand=[
                        'SSH_PUBKEY="{}"'.format(pubkey),
                        'echo $SSH_PUBKEY >> ~ec2-user/.ssh/authorized_keys',
                    ]
                )
            )
        ]
    )
    return json.dumps(document)


"""
def upload_document(
response = client.create_document(
    Content='string',
    Name='string',
    DocumentType='Command'|'Policy'|'Automation',
    DocumentFormat='YAML'|'JSON',
    TargetType='string'
)

def main():
    pubkey = read_public_key_from_file(DEFAULT_PUBKEY)
    set_encrypted_param('ssh_pubkey', pubkey)
"""
