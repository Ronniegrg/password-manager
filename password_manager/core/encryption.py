"""
Encryption functionality for secure password storage
"""
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class Encryption:
    def __init__(self):
        self.key = None
        self.fernet = None

    def initialize(self, master_password):
        # Generate a key from the master password
        salt = b'password_manager_salt'  # In production, use a secure random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.key = key
        self.fernet = Fernet(key)

    def encrypt(self, data):
        if not self.fernet:
            raise ValueError("Encryption not initialized")
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        if not self.fernet:
            raise ValueError("Encryption not initialized")
        return self.fernet.decrypt(encrypted_data.encode()).decode()
