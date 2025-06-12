"""
Custom widgets for the Password Manager GUI
"""
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QHBoxLayout, QWidget,
                             QCheckBox)
from PyQt5.QtCore import Qt


class PasswordLineEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Show/Hide button
        self.show_btn = QPushButton('Show')
        self.show_btn.setCheckable(True)
        self.show_btn.clicked.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_btn)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_btn.setText('Hide')
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_btn.setText('Show')

    def text(self):
        return self.password_input.text()

    def setText(self, text):
        self.password_input.setText(text)


class CopyButton(QPushButton):
    def __init__(self, text="Copy", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)


class DeleteButton(QPushButton):
    def __init__(self, text="Delete", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41810;
            }
        """)


class GenerateButton(QPushButton):
    def __init__(self, text="Generate", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
