from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Generate RSA key pair (private and public keys)
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("private.pem", "wb") as priv_file:
        priv_file.write(private_key)
    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key)

    return private_key, public_key

# Encrypt AES key using the recipient's public RSA key
def encrypt_aes_key(aes_key, public_key_path):
    with open(public_key_path, "rb") as file:
        public_key = RSA.import_key(file.read())

    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    return base64.b64encode(encrypted_key)

# Decrypt AES key using the recipient's private RSA key
def decrypt_aes_key(encrypted_key, private_key_path):
    with open(private_key_path, "rb") as file:
        private_key = RSA.import_key(file.read())

    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_key = cipher_rsa.decrypt(base64.b64decode(encrypted_key))
    return decrypted_key