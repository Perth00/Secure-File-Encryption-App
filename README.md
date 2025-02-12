# Secure-File-Encryption-App
The Secure File Encryption App is a Python-based application designed to securely encrypt and decrypt files using AES (Advanced Encryption Standard) and RSA (Rivest–Shamir–Adleman) algorithms. It also includes a secure login system to ensure that only authorized users can access the app.


🚀 Features

User Authentication: Secure login and registration system with password hashing (SHA-256).
File Encryption: AES-based file encryption with automatic deletion of the original file after encryption.
File Decryption: AES decryption with automatic deletion of the encrypted file after decryption.
Secure File Sharing: RSA-based key encryption for secure file sharing.
Key Management: Automatic deletion of RSA key files after decryption.
Clean GUI: User-friendly interface built with Tkinter.

![{A256A385-81C0-41AA-87BA-9D53BC7B196A}](https://github.com/user-attachments/assets/311620b2-865b-4acd-ac5e-c7e7727d8e35)


User Authentication
Register: Create a new account.
Login: Log in with your credentials to access the main app.
File Operations
Select File: Choose the file you want to encrypt or decrypt.
Encrypt File: Encrypt the selected file (original file will be deleted).
Decrypt File: Decrypt an encrypted file (encrypted file will be deleted).
Secure File Sharing
Generate RSA Keys: Create a pair of RSA keys.
Secure Share File: Encrypt the AES key with the RSA public key.
Decrypt Shared Key: Decrypt the shared AES key using the RSA private key.

🔐 Security Features
Passwords are hashed using SHA-256.
AES encryption with secure key handling.
RSA encryption for secure key exchange.
Automatic deletion of sensitive files (original files, encrypted files, RSA keys).


🙏 Acknowledgements
Python
PyCryptodome
Tkinter

