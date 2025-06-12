"""
Window for deleting passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt


class DeletePasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Delete Password')
        self.setFixedSize(400, 200)

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

        # Delete button
        self.delete_btn = QPushButton('Delete Password')
        self.delete_btn.clicked.connect(self.delete_password)
        layout.addWidget(self.delete_btn)

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

    def delete_password(self):
        website = self.website_combo.currentText()

        if not website:
            QMessageBox.warning(self, 'Error', 'Please select a website')
            return

        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete the password for {website}?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                if self.parent.password_manager.delete_password(website):
                    QMessageBox.information(
                        self, 'Success', 'Password deleted successfully')
                    self.update_website_list()
                    self.accept()
                else:
                    QMessageBox.warning(
                        self, 'Error', 'Failed to delete password')
            except Exception as e:
                QMessageBox.warning(
                    self, 'Error', f'Failed to delete password: {str(e)}')
