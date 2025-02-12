import hashlib
import json
import os

# Path to store user credentials
CREDENTIALS_FILE = "users.json"

# Hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
def register(username, password):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        return False, "Username already exists."

    users[username] = hash_password(password)

    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(users, file)

    return True, "Registration successful."

# Authenticate user login
def authenticate(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        return False, "No registered users found."

    with open(CREDENTIALS_FILE, "r") as file:
        users = json.load(file)

    if username in users and users[username] == hash_password(password):
        return True, "Login successful."
    else:
        return False, "Invalid username or password."
