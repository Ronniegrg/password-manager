"""
Initial setup window for the Password Manager
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from ..core.encryption import Encryption
from ..config.settings import Settings


class SetupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.encryption = Encryption()
        self.settings = Settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Initial Setup')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel('Please set up your master password:')
        layout.addWidget(instructions)

        # Password input
        self.password_label = QLabel('Master Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Confirm password input
        self.confirm_label = QLabel('Confirm Password:')
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_label)
        layout.addWidget(self.confirm_input)

        # Setup button
        self.setup_button = QPushButton('Setup')
        self.setup_button.clicked.connect(self.setup_password)
        layout.addWidget(self.setup_button)

        self.setLayout(layout)

    def setup_password(self):
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not password or not confirm:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        if password != confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            self.password_input.clear()
            self.confirm_input.clear()
            return

        try:
            self.encryption.initialize(password)
            self.parent.password_manager.encryption = self.encryption
            self.settings.set("encryption_key", password)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Failed to setup encryption')
            self.password_input.clear()
            self.confirm_input.clear()
