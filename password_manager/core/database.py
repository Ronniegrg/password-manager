"""
Database functionality for storing password entries
"""
import json
import os
from ..config.settings import Settings


class Database:
    def __init__(self):
        self.settings = Settings()
        self.db_file = self.settings.get("database_path", "passwords.json")
        self.data = self.load_database()

    def load_database(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_database(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_entry(self, website, username, encrypted_password):
        if website in self.data:
            return False
        self.data[website] = {
            'username': username,
            'password': encrypted_password
        }
        self.save_database()
        return True

    def get_entry(self, website):
        return self.data.get(website)

    def update_entry(self, website, encrypted_password):
        if website not in self.data:
            return False
        self.data[website]['password'] = encrypted_password
        self.save_database()
        return True

    def delete_entry(self, website):
        if website not in self.data:
            return False
        del self.data[website]
        self.save_database()
        return True

    def list_websites(self):
        return list(self.data.keys())
