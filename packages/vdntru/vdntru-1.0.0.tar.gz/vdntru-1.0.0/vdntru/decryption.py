# -*- coding: utf-8 -*-
# Step 3: AES Decryption
"decryption.py"
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import base64

def aes_decrypt(encrypted_data, key):
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv = encrypted_data_bytes[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data_bytes[16:]) + decryptor.finalize()
    return decrypted_data.decode()



# NTRU Decryption for all data
def NTRU_decryption(encrypted_data, aes_key):
    # Decrypt data using AES
    decrypted_data = aes_decrypt(encrypted_data, aes_key)
    return decrypted_data




def ntrudecryption(Data,decrypted_aes_key):
    
    Decrypted_data = NTRU_decryption(Data, decrypted_aes_key)
    return Decrypted_data
    