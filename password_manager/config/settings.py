"""
Configuration settings for the Password Manager
"""
import json
import os


class Settings:
    def __init__(self):
        self.config_file = "config.json"
        self.default_settings = {
            "database_path": "passwords.json",
            "encryption_key": None,
            "theme": "light",
            "auto_lock_timeout": 300,  # 5 minutes
            "clipboard_timeout": 30,   # 30 seconds
        }
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.default_settings.copy()
        return self.default_settings.copy()

    def save_settings(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
