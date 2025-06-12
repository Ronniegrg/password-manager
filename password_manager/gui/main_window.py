"""
Main window of the Password Manager application
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QMessageBox, QLabel, QHBoxLayout, QFrame, QSplitter,
                             QStackedWidget, QToolButton, QScrollArea)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPalette
from .login_window import LoginWindow
from .setup_window import SetupWindow
from ..core.password_manager import PasswordManager
from ..config.settings import Settings
from .settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.password_manager = PasswordManager()
        self.init_ui()
        # Load and apply the saved theme settings
        self.load_appearance_settings()

    def init_ui(self):
        self.setWindowTitle('Password Manager')
        self.setGeometry(100, 100, 900, 600)  # Larger default size
        self.setMinimumSize(800, 500)

        # Apply a modern application-wide style
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f5f6fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QToolTip {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 5px;
            }
        ''')

        # Main horizontal layout with splitter
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create main container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # === Left Sidebar ===
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet('''
            #sidebar {
                background-color: #2c3e50;
                min-width: 240px;
                max-width: 240px;
                padding: 0;
            }
        ''')
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # App logo and title in sidebar
        logo_container = QFrame()
        logo_container.setStyleSheet(
            "background-color: #243342; padding: 15px;")
        logo_layout = QHBoxLayout(logo_container)

        from .settings_dialog import SettingsDialog
        self.settings_btn = QToolButton()
        self.settings_btn.setIcon(QIcon('D:\\Independant Projects\\password-manager\\settings.png'))
        self.settings_btn.setIconSize(QSize(32, 32))
        self.settings_btn.setToolTip('Settings')
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.setStyleSheet('''
            QToolButton {
                background-color: transparent;
                border: none;
            }
            QToolButton:hover {
                background-color: #34495e;
                border-radius: 4px;
            }
        ''')
        self.settings_btn.clicked.connect(self.show_settings_dialog)
        logo_layout.addWidget(self.settings_btn)

        app_title = QLabel("Password Vault")
        app_title.setStyleSheet(
            "color: white; font-size: 18px; font-weight: bold;")

        logo_layout.addWidget(app_title)
        logo_layout.addStretch()

        sidebar_layout.addWidget(logo_container)

        # Navigation buttons
        nav_buttons_container = QWidget()
        nav_layout = QVBoxLayout(nav_buttons_container)
        nav_layout.setContentsMargins(8, 20, 8, 10)
        nav_layout.setSpacing(4)

        # Navigation button style
        nav_button_style = '''
            QPushButton {
                background-color: transparent;
                color: #b2bec3;
                border: none;
                border-radius: 5px;
                padding: 12px 15px;
                text-align: left;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
            }
        '''

        # Add navigation buttons with icons
        # Create function to add nav buttons more easily
        def create_nav_button(text, icon_name, slot):
            button = QPushButton(text)
            button.setStyleSheet(nav_button_style)
            # Set icon if icon exists
            button.setCheckable(True)
            button.setIconSize(QSize(20, 20))
            # Connect to slot
            button.clicked.connect(slot)
            nav_layout.addWidget(button)
            return button

        self.add_btn = create_nav_button(
            "Add Password", "add", self.show_add_password_window)
        self.get_btn = create_nav_button(
            "Get Password", "retrieve", self.show_retrieve_password_window)
        self.update_btn = create_nav_button(
            "Update Password", "update", self.show_update_password_window)
        self.delete_btn = create_nav_button(
            "Delete Password", "delete", self.show_delete_password_window)
        self.list_btn = create_nav_button(
            "List Websites", "list", self.show_list_websites_window)

        # Add spacing and stretch at the bottom
        nav_layout.addStretch(1)

        # Version info at bottom of sidebar
        version_label = QLabel("v2.0")
        version_label.setStyleSheet("color: #546E7A; padding: 15px;")
        version_label.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(nav_buttons_container)
        sidebar_layout.addWidget(version_label, 0, Qt.AlignBottom)

        # === Main Content Area ===
        content_area = QFrame()
        content_area.setObjectName("content_area")
        content_area.setStyleSheet('''
            #content_area {
                background-color: white;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
            }
        ''')

        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 20)

        # Welcome header
        header_label = QLabel("Welcome to Your Password Vault")
        header_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #34495e; margin-bottom: 10px;")

        subheader_label = QLabel(
            "Securely manage all your passwords in one place")
        subheader_label.setStyleSheet(
            "font-size: 16px; color: #7f8c8d; margin-bottom: 25px;")

        # Dashboard cards
        cards_container = QFrame()
        cards_container.setObjectName("cards_container")
        cards_layout = QHBoxLayout(cards_container)

        # Function to create info cards
        def create_info_card(title, value, color):
            card = QFrame()
            card.setStyleSheet(f'''
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
            ''')
            card_layout = QVBoxLayout(card)

            title_label = QLabel(title)
            title_label.setStyleSheet("color: white; font-size: 16px;")

            value_label = QLabel(value)
            value_label.setStyleSheet(
                "color: white; font-size: 24px; font-weight: bold;")

            card_layout.addWidget(title_label)
            card_layout.addWidget(value_label)
            card_layout.addStretch()

            return card

        # Get password count
        try:
            password_count = str(len(self.password_manager.get_all_websites()))
        except:
            password_count = "0"

        cards_layout.addWidget(create_info_card(
            "Total Passwords", password_count, "#3498db"))
        cards_layout.addWidget(create_info_card(
            "Security Score", "Strong", "#2ecc71"))
        cards_layout.addWidget(create_info_card(
            "Last Update", "Today", "#9b59b6"))

        # Quick actions section
        actions_container = QFrame()
        actions_container.setStyleSheet('''
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
        ''')
        actions_layout = QVBoxLayout(actions_container)

        actions_header = QLabel("Quick Actions")
        actions_header.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        actions_layout.addWidget(actions_header)

        quick_actions_layout = QHBoxLayout()

        # Quick action button style
        quick_btn_style = '''
            QPushButton {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f5f6fa;
                border-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #ebedf0;
            }
        '''

        new_password_btn = QPushButton("New Password")
        new_password_btn.setStyleSheet(quick_btn_style)
        new_password_btn.clicked.connect(self.show_add_password_window)

        search_btn = QPushButton("Search Passwords")
        search_btn.setStyleSheet(quick_btn_style)
        search_btn.clicked.connect(self.show_retrieve_password_window)

        view_all_btn = QPushButton("View All")
        view_all_btn.setStyleSheet(quick_btn_style)
        view_all_btn.clicked.connect(self.show_list_websites_window)

        quick_actions_layout.addWidget(new_password_btn)
        quick_actions_layout.addWidget(search_btn)
        quick_actions_layout.addWidget(view_all_btn)

        actions_layout.addLayout(quick_actions_layout)

        # Add all components to content layout
        content_layout.addWidget(header_label)
        content_layout.addWidget(subheader_label)
        content_layout.addWidget(cards_container)
        content_layout.addSpacing(20)
        content_layout.addWidget(actions_container)
        content_layout.addStretch()

        # Footer
        footer = QLabel(
            "© 2025 Password Vault | Your passwords stay secure and private")
        footer.setStyleSheet("color: #95a5a6; font-size: 12px;")
        footer.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(footer)

        # Add sidebar and content area to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area, 1)  # Content area should expand

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

    def show_settings_dialog(self):
        dlg = SettingsDialog(self)
        dlg.exec_()

    def load_appearance_settings(self):
        """Load and apply the saved appearance settings."""
        theme = self.settings.get("theme", "light")
        font_family = self.settings.get("font_family", "Segoe UI")
        font_size = self.settings.get("font_size", 10)

        # Apply font settings
        from PyQt5.QtGui import QFont
        app_font = QFont(font_family, font_size)
        self.setFont(app_font)

        # Apply theme
        if theme == "dark":
            self.apply_dark_theme()
        elif theme == "light":
            self.apply_light_theme()
        elif theme == "system":
            # For system theme, we'll just use light for now
            self.apply_light_theme()

    def apply_light_theme(self):
        """Apply light theme to the application."""
        from PyQt5.QtGui import QColor, QPalette

        # Update the main stylesheet
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f5f6fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QToolTip {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 5px;
            }
        ''')

        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.WindowText, QColor(10, 10, 10))
        light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.Text, QColor(10, 10, 10))
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, QColor(10, 10, 10))
        light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        self.setPalette(light_palette)

    def apply_dark_theme(self):
        """Apply dark theme to the application."""
        from PyQt5.QtGui import QColor, QPalette

        # Update the main stylesheet
        self.setStyleSheet('''
            QMainWindow {
                background-color: #1e272e;
            }
            QLabel {
                color: #dcdde1;
            }
            QToolTip {
                background-color: #dcdde1;
                color: #1e272e;
                border: none;
                padding: 5px;
            }
            QWidget {
                background-color: #1e272e;
                color: #dcdde1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit, QComboBox, QSpinBox {
                border: 1px solid #3f4a56;
                background-color: #2d3436;
                color: #dcdde1;
                padding: 5px;
                border-radius: 3px;
            }
            QTableView {
                background-color: #2d3436;
                color: #dcdde1;
                gridline-color: #3f4a56;
                border: 1px solid #3f4a56;
            }
            QHeaderView::section {
                background-color: #3f4a56;
                color: #dcdde1;
                padding: 5px;
                border: 1px solid #2d3436;
            }
        ''')

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        self.setPalette(dark_palette)
