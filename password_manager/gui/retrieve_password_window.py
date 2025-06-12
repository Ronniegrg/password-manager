"""
Window for retrieving passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ..utils.clipboard_manager import ClipboardManager


class RetrievePasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.clipboard = ClipboardManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Retrieve Password')
        self.setFixedSize(440, 340)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(10)

        # Header
        header = QLabel('🔍 Retrieve Password')
        header.setStyleSheet(
            'font-size: 22px; font-weight: bold; margin-bottom: 10px;')
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Card/frame for form
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background: #f8f9fa;
                border-radius: 14px;
                border: 1px solid #e0e0e0;
            }
        ''')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 18, 28, 18)
        card_layout.setSpacing(12)

        # Website selection
        self.website_label = QLabel('Select Website:')
        self.website_combo = QComboBox()
        self.update_website_list()
        card_layout.addWidget(self.website_label)
        card_layout.addWidget(self.website_combo)

        # Username display
        self.username_label = QLabel('Username:')
        self.username_display = QLineEdit()
        self.username_display.setReadOnly(True)
        card_layout.addWidget(self.username_label)
        card_layout.addWidget(self.username_display)

        # Password display
        self.password_label = QLabel('Password:')
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_label)
        card_layout.addWidget(self.password_display)

        # Button style
        btn_style = '''
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 0;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        '''

        # Buttons row
        btn_row = QHBoxLayout()
        self.copy_btn = QPushButton('Copy Password')
        self.copy_btn.setStyleSheet(btn_style)
        self.copy_btn.setIcon(QIcon.fromTheme('edit-copy'))
        self.copy_btn.clicked.connect(self.copy_password)
        btn_row.addWidget(self.copy_btn)

        self.show_btn = QPushButton('Show Password')
        self.show_btn.setStyleSheet(btn_style)
        self.show_btn.setIcon(QIcon.fromTheme('view-password'))
        self.show_btn.clicked.connect(self.toggle_password_visibility)
        btn_row.addWidget(self.show_btn)

        card_layout.addLayout(btn_row)
        main_layout.addWidget(card)

        # Connect website selection change
        self.website_combo.currentTextChanged.connect(self.update_credentials)

        self.setLayout(main_layout)

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
                self.password_display.setText(entry['password'])
            else:
                self.username_display.clear()
                self.password_display.clear()
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to retrieve credentials: {str(e)}')

    def copy_password(self):
        password = self.password_display.text()
        if password:
            self.clipboard.copy_to_clipboard(password)
            QMessageBox.information(
                self, 'Success', 'Password copied to clipboard')
        else:
            QMessageBox.warning(self, 'Error', 'No password to copy')

    def toggle_password_visibility(self):
        if self.password_display.echoMode() == QLineEdit.Password:
            self.password_display.setEchoMode(QLineEdit.Normal)
            self.show_btn.setText('Hide Password')
        else:
            self.password_display.setEchoMode(QLineEdit.Password)
            self.show_btn.setText('Show Password')
