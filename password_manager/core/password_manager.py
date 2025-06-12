"""
Core password manager functionality
"""
from .database import Database
from .encryption import Encryption
from ..utils.password_generator import generate_password


class PasswordManager:
    def __init__(self):
        self.db = Database()
        self.encryption = Encryption()

    def add_password(self, website, username, password):
        encrypted_password = self.encryption.encrypt(password)
        return self.db.add_entry(website, username, encrypted_password)

    def get_password(self, website):
        entry = self.db.get_entry(website)
        if entry:
            return self.encryption.decrypt(entry['password'])
        return None

    def update_password(self, website, new_password):
        encrypted_password = self.encryption.encrypt(new_password)
        return self.db.update_entry(website, encrypted_password)

    def delete_password(self, website):
        return self.db.delete_entry(website)

    def list_websites(self):
        return self.db.list_websites()

    def generate_secure_password(self, length=16):
        return generate_password(length)
