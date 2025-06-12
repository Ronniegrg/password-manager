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
                    data = json.load(f)

                    # Handle legacy format with "passwords" array
                    if "passwords" in data and isinstance(data["passwords"], list):
                        # Convert array format to dict format
                        converted_data = {}
                        for entry in data["passwords"]:
                            if "website" in entry:
                                website = entry["website"]
                                converted_data[website] = {
                                    'username': entry.get('username', ''),
                                    'password': entry.get('password', ''),
                                    'url': entry.get('url', ''),
                                    'email': entry.get('email', ''),
                                    'additional_info': entry.get('additional_info', '')
                                }
                        return converted_data

                    return data
            except json.JSONDecodeError:
                return {}
        return {}

    def save_database(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_entry(self, website, username, encrypted_password, url='', email='', additional_info=''):
        if website in self.data:
            return False
        self.data[website] = {
            'username': username,
            'password': encrypted_password,
            'url': url,
            'email': email,
            'additional_info': additional_info
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

    def update_entry_full(self, old_website, new_website, username, encrypted_password, url, email, additional_info):
        if old_website not in self.data:
            return False
        # If website name is changed, move the entry
        if old_website != new_website:
            if new_website in self.data:
                return False  # Don't overwrite existing
            self.data[new_website] = self.data.pop(old_website)
        self.data[new_website] = {
            'username': username,
            'password': encrypted_password,
            'url': url,
            'email': email,
            'additional_info': additional_info
        }
        self.save_database()
        return True
