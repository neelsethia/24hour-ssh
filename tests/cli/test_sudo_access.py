import sys
import os

#from main.sudo_access import generate_key_crypto
from ec2ssh.cli.sudo_access import generate_key_paramiko
from ec2ssh.cli.sudo_access import target_prompt_selector
from ec2ssh.cli.sudo_access import transfer_key 
from ec2ssh import ssm 
from ec2ssh import prompter

# def test_generated_crypto_key():
    
#     #generating key and then testing to see whether we see the file in the cwd. 
#     generate_key_crypto()
    
#     #public key check 
#     assert os.path.isfile("private.key")
#     assert os.path.isfile("public.key")
    
def test_generated_para_key():
    
    generate_key_paramiko("private.key", "hello")
    
    #assert os.path.isfile("private.key")
    #assert os.path.isfile("pkey.pub")

def real_time_ssm_test(): 
    #prompt for instance
    instanceId = target_prompt_selector()
    transfer_key(instanceId)
    
    #test to see whether key is in selected instance (instanceId: 'i-05c53b1387a292ba7' <- put in here once determined) 
    
    
    
if __name__ == '__main__':
    test_generated_para_key()
    real_time_ssm_test()