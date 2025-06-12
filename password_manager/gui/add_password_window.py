"""
Window for adding new passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from ..utils.password_generator import generate_password
from ..utils.clipboard_manager import ClipboardManager


class AddPasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.clipboard = ClipboardManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add Password')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Website input
        self.website_label = QLabel('Website:')
        self.website_input = QLineEdit()
        layout.addWidget(self.website_label)
        layout.addWidget(self.website_input)

        # Username input
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password input
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Generate password button
        self.generate_btn = QPushButton('Generate Password')
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        # Add button
        self.add_btn = QPushButton('Add Password')
        self.add_btn.clicked.connect(self.add_password)
        layout.addWidget(self.add_btn)

        self.setLayout(layout)

    def generate_password(self):
        password = generate_password()
        self.password_input.setText(password)
        self.clipboard.copy_to_clipboard(password)
        QMessageBox.information(
            self, 'Success', 'Password generated and copied to clipboard')

    def add_password(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not all([website, username, password]):
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        try:
            if self.parent.password_manager.add_password(website, username, password):
                QMessageBox.information(
                    self, 'Success', 'Password added successfully')
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Website already exists')
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to add password: {str(e)}')
