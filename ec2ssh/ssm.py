import os
import boto3
import json


def read_public_key_from_file(pubkey_file):
    with open(pubkey_file, 'r') as pubkey:
        return pubkey.read()


def get_ssm_client():
    return boto3.client('ssm', 'us-west-2') #, aws_access_key_id="", aws_secret_access_key="")


def build_document(pubkey):
    document = dict(
        schemaVersion='2.2',
        description='Install ssh public key into ~ec2-user/.ssh/authorized_keys',
        parameters=dict(),
        mainSteps=[
            dict(
                action='aws:runShellScript',
                name='sshPubkeySetup',
                inputs=dict(
                    runCommand=[
                        'SSH_PUBKEY="{}"'.format(pubkey),
                        'echo $SSH_PUBKEY >> ~ec2-user/.ssh/authorized_keys',
                    ]
                )
            )
        ]
    )
    return json.dumps(document)

def upload_document(client, document_name, document):
    try:
        client.create_document(
            Content=document,
            Name='sshPubkeySetup',
            DocumentType='Command',
            DocumentFormat='JSON',
            TargetType='/AWS::EC2::Instance'
        )
    except client.exceptions.DocumentAlreadyExists:
        pass
    return

def send_command(client, instance_id):
    response = client.send_command(
        InstanceIds=[instance_id],
        DocumentName='sshPubkeySetup',
        TimeoutSeconds=3600,
        Parameters=dict(),
    )
    return response


def main():
    client = boto3.client('ssm', 'us-west-2')
    pubkey_file = '~/.ssh/id_rsa.pub'
    pubkey = read_public_key_from_file(os.path.expanduser(pubkey_file))
    document = build_document(pubkey)
    document_name = 'sshPubkeySetup'
    upload_document(client, document_name, document)
    # for instance in get_24hourssh_enabled_instances():
    #     print(instance.id)
    
    


if __name__ == '__main__':
    main()
