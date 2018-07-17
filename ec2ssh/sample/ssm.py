import boto3 


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

