"""
Main window of the Password Manager application
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QMessageBox)
from PyQt5.QtCore import Qt
from .login_window import LoginWindow
from .setup_window import SetupWindow
from ..core.password_manager import PasswordManager
from ..config.settings import Settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.password_manager = PasswordManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Password Manager')
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(500, 400)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 30, 40, 20)
        main_layout.setSpacing(20)

        # Header with icon and title
        from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame
        from PyQt5.QtGui import QPixmap
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_pixmap = QPixmap('settings.png').scaled(40, 40)
        icon_label.setPixmap(icon_pixmap)
        title_label = QLabel('Password Manager')
        title_label.setStyleSheet(
            'font-size: 28px; font-weight: bold; margin-left: 12px;')
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Card/frame for main actions
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background: #f8f9fa;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }
        ''')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(18)

        # Modern button style
        btn_style = '''
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 0;
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

        # Add action buttons
        add_btn = QPushButton('Add Password', self)
        add_btn.setStyleSheet(btn_style)
        add_btn.clicked.connect(self.show_add_password_window)
        card_layout.addWidget(add_btn)

        get_btn = QPushButton('Get Password', self)
        get_btn.setStyleSheet(btn_style)
        get_btn.clicked.connect(self.show_retrieve_password_window)
        card_layout.addWidget(get_btn)

        update_btn = QPushButton('Update Password', self)
        update_btn.setStyleSheet(btn_style)
        update_btn.clicked.connect(self.show_update_password_window)
        card_layout.addWidget(update_btn)

        delete_btn = QPushButton('Delete Password', self)
        delete_btn.setStyleSheet(btn_style)
        delete_btn.clicked.connect(self.show_delete_password_window)
        card_layout.addWidget(delete_btn)

        list_btn = QPushButton('List Websites', self)
        list_btn.setStyleSheet(btn_style)
        list_btn.clicked.connect(self.show_list_websites_window)
        card_layout.addWidget(list_btn)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignHCenter)
        main_layout.addStretch()

        # Footer/status bar
        footer = QLabel(
            '© 2024 Password Manager | Your passwords stay safe and local.')
        footer.setStyleSheet('color: #888; font-size: 12px; margin-top: 10px;')
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        # Check if first run
        if not self.settings.get("encryption_key"):
            self.show_setup_window()
        else:
            self.show_login_window()

    def show_setup_window(self):
        self.setup_window = SetupWindow(self)
        self.setup_window.show()

    def show_login_window(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()

    def show_add_password_window(self):
        from .add_password_window import AddPasswordWindow
        self.add_window = AddPasswordWindow(self)
        self.add_window.show()

    def show_retrieve_password_window(self):
        from .retrieve_password_window import RetrievePasswordWindow
        self.retrieve_window = RetrievePasswordWindow(self)
        self.retrieve_window.show()

    def show_update_password_window(self):
        from .update_password_window import UpdatePasswordWindow
        self.update_window = UpdatePasswordWindow(self)
        self.update_window.show()

    def show_delete_password_window(self):
        from .delete_password_window import DeletePasswordWindow
        self.delete_window = DeletePasswordWindow(self)
        self.delete_window.show()

    def show_list_websites_window(self):
        from .list_websites_window import ListWebsitesWindow
        self.list_window = ListWebsitesWindow(self)
        self.list_window.show()
