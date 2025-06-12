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

    def add_password(self, website, username, password, url='', email='', additional_info=''):
        encrypted_password = self.encryption.encrypt(password)
        return self.db.add_entry(website, username, encrypted_password, url, email, additional_info)

    def get_password(self, website):
        entry = self.db.get_entry(website)
        if entry:
            result = dict(entry)
            try:
                result['password'] = self.encryption.decrypt(entry['password'])
                result['decryption_error'] = False
            except Exception:
                result['decryption_error'] = True
            return result
        return None

    def list_websites(self):
        return self.db.list_websites()

    def generate_secure_password(self, length=16):
        return generate_password(length)
