from cryptography.fernet import Fernet

# Generate a key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt a file
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(file_path + ".enc", 'wb') as file:
        file.write(encrypted_data)

# Decrypt a file
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path[:-4], 'wb') as file:
        file.write(decrypted_data)
