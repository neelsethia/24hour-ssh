import sys 
import os

#from main.sudo_access import generate_key_crypto
from main.sudo_access import generate_key_paramiko


# def test_generated_crypto_key():
    
#     #generating key and then testing to see whether we see the file in the cwd. 
#     generate_key_crypto()
    
#     #public key check 
#     assert os.path.isfile("private.key")
#     assert os.path.isfile("public.key")
    
def test_generated_para_key():
    
    generate_key_paramiko("private.key", "hello")
    
    assert os.path.isfile("private.key")
    assert os.path.isfile("pkey.pub")
    
if __name__ == '__test__':
    test_generated_para_key()