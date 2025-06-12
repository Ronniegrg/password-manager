"""
Password strength indicator widget
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class PasswordStrengthWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Strength label
        self.strength_label = QLabel('Password Strength:')
        layout.addWidget(self.strength_label)

        # Progress bar
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setTextVisible(False)
        layout.addWidget(self.strength_bar)

        self.setLayout(layout)

    def update_strength(self, password):
        if not password:
            self.strength_bar.setValue(0)
            self.strength_bar.setStyleSheet("")
            return

        # Calculate password strength
        strength = 0
        if len(password) >= 8:
            strength += 20
        if any(c.isupper() for c in password):
            strength += 20
        if any(c.islower() for c in password):
            strength += 20
        if any(c.isdigit() for c in password):
            strength += 20
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 20

        # Update progress bar
        self.strength_bar.setValue(strength)

        # Set color based on strength
        if strength < 40:
            color = "#ff0000"  # Red
        elif strength < 60:
            color = "#ffa500"  # Orange
        elif strength < 80:
            color = "#ffff00"  # Yellow
        else:
            color = "#00ff00"  # Green

        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #999;
                border-radius: 3px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
