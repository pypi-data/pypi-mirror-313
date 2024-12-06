from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
"encryption.py"
# Step 1: Key Generation
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

# Step 2: AES Encryption
def aes_encrypt(data, key):
    iv = os.urandom(16)  # 16-byte IV for AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data)  # IV + Encrypted Data

# Step 3: AES Decryption
def aes_decrypt(encrypted_data, key):
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv = encrypted_data_bytes[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data_bytes[16:]) + decryptor.finalize()
    return decrypted_data.decode()

# Step 4: Encrypt AES key using RSA
def encrypt_aes_key(public_key_pem, aes_key):
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_key)

# Step 5: Decrypt AES key using RSA
def decrypt_aes_key(private_key_pem, encrypted_aes_key):
    private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
    encrypted_key_bytes = base64.b64decode(encrypted_aes_key)
    aes_key = private_key.decrypt(
        encrypted_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key

# NTRU Encryption for all data
def NTRU_encryption(data, aes_key, public_key_pem):
    # Encrypt data using AES
    encrypted_data = aes_encrypt(data, aes_key)
    return encrypted_data

# NTRU Decryption for all data
def NTRU_decryption(encrypted_data, aes_key):
    # Decrypt data using AES
    decrypted_data = aes_decrypt(encrypted_data, aes_key)
    return decrypted_data


private_key_pem, public_key_pem = generate_keys()
 
# Generate RSA and AES keys once
def ntruencryption(Data):

    aes_key = os.urandom(32)  # 256-bit AES key
    encrypted_aes_key = encrypt_aes_key(public_key_pem, aes_key)
    encrypted_data = NTRU_encryption(Data, aes_key, public_key_pem)
    
    # Decrypt all data using the same keys
    decrypted_aes_key = decrypt_aes_key(private_key_pem, encrypted_aes_key)
    
    return encrypted_data,decrypted_aes_key,public_key_pem


    


