import os 
import boto3 


def is_24hourssh_enabled(instance):
    is_enabled = next((
            True for tag in instance.tags
            if tag['Key'] == '24hourssh'
            and tag['Value'] == 'enabled'
        ), False)
    return is_enabled

def get_24hourssh_enabled_instances():
    ec2 = boto3.resource('ec2', region_name='us-west-2')
    return [
        instance for instance in ec2.instances.all()
        if instance.state['Name'] == 'running'
        and is_24hourssh_enabled(instance)
    ]

def compare_24hourssh_enabled_instance_ID(instanceID):
    ec2=boto3.resource('ec2',region_name='us-west-2')
    for instance in ec2.instances.all():
        if (instance.id == instanceID 
        and instance.state['Name'] == 'running' 
        and is_24hourssh_enabled(instance)):
                return True
    return False
    
def test_output():
    ec2=boto3.resource('ec2',region_name='us-west-2')
    for instance in ec2.instances.all():
        if is_24hourssh_enabled(instance):
            print(instance.id) 
