"""
Window for updating passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from ..utils.password_generator import generate_password
from ..utils.clipboard_manager import ClipboardManager


class UpdatePasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.clipboard = ClipboardManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Update Password')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Website selection
        self.website_label = QLabel('Select Website:')
        self.website_combo = QComboBox()
        self.update_website_list()
        layout.addWidget(self.website_label)
        layout.addWidget(self.website_combo)

        # Username display
        self.username_label = QLabel('Username:')
        self.username_display = QLineEdit()
        self.username_display.setReadOnly(True)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_display)

        # New password input
        self.password_label = QLabel('New Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Generate password button
        self.generate_btn = QPushButton('Generate Password')
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        # Update button
        self.update_btn = QPushButton('Update Password')
        self.update_btn.clicked.connect(self.update_password)
        layout.addWidget(self.update_btn)

        # Connect website selection change
        self.website_combo.currentTextChanged.connect(self.update_credentials)

        self.setLayout(layout)

    def update_website_list(self):
        self.website_combo.clear()
        websites = self.parent.password_manager.list_websites()
        self.website_combo.addItems(websites)

    def update_credentials(self, website):
        if not website:
            return

        try:
            entry = self.parent.password_manager.get_password(website)
            if entry:
                self.username_display.setText(entry['username'])
            else:
                self.username_display.clear()
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to retrieve credentials: {str(e)}')

    def generate_password(self):
        password = generate_password()
        self.password_input.setText(password)
        self.clipboard.copy_to_clipboard(password)
        QMessageBox.information(
            self, 'Success', 'Password generated and copied to clipboard')

    def update_password(self):
        website = self.website_combo.currentText()
        new_password = self.password_input.text()

        if not website or not new_password:
            QMessageBox.warning(
                self, 'Error', 'Please select a website and enter a new password')
            return

        try:
            if self.parent.password_manager.update_password(website, new_password):
                QMessageBox.information(
                    self, 'Success', 'Password updated successfully')
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to update password')
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to update password: {str(e)}')
