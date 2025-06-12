"""
Login window for the Password Manager
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from ..core.encryption import Encryption
from .widgets.custom_widgets import PasswordLineEdit


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.encryption = Encryption()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setFixedSize(380, 230)
        self.setStyleSheet('background: #f4f6fa;')

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(0)

        # Header
        header = QLabel('🔒 Login')
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            'font-size: 22px; font-weight: bold; margin-bottom: 10px;')
        main_layout.addWidget(header)

        # Card/frame for form
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background: #fff;
                border-radius: 14px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }
        ''')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 22, 28, 22)
        card_layout.setSpacing(16)

        # Password label and input
        self.password_label = QLabel('Master Password:')
        self.password_label.setStyleSheet('font-size: 15px; font-weight: 500;')
        card_layout.addWidget(self.password_label)

        self.password_input = PasswordLineEdit()
        card_layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton('Login')
        btn_style = '''
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 0;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        '''
        self.login_button.setStyleSheet(btn_style)
        self.login_button.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_button.setMinimumHeight(38)
        self.login_button.clicked.connect(self.verify_password)
        card_layout.addWidget(self.login_button)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignHCenter)
        main_layout.addStretch()

    def verify_password(self):
        password = self.password_input.text()
        try:
            self.encryption.initialize(password)
            self.parent.password_manager.encryption = self.encryption
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Invalid master password')
            self.password_input.setText("")
