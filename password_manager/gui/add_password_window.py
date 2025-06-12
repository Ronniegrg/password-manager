"""
Window for adding new passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QFrame, QHBoxLayout,
                             QScrollArea, QWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QIcon
from ..utils.password_generator import generate_password
from ..utils.clipboard_manager import ClipboardManager


class AddPasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.clipboard = ClipboardManager()
        self.setWindowFlags(
            Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add Password')
        self.setFixedSize(500, 580)  # Increased size for better spacing

        # Set window style with a cleaner look
        self.setStyleSheet('''
            QDialog {
                background-color: #f8fafc;
            }
        ''')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Create header with shadow effect
        header_container = QFrame()
        header_container.setStyleSheet('''
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: none;
            }
        ''')

        # Add shadow effect to header
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(15, 23, 42, 20))
        shadow.setOffset(0, 4)
        header_container.setGraphicsEffect(shadow)

        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(20, 20, 20, 20)

        # Enhanced Header with icon
        title_layout = QHBoxLayout()
        header_icon = QLabel()
        header_icon.setText("🔑")
        header_icon.setStyleSheet('font-size: 28px; margin-right: 12px;')
        title_layout.addWidget(header_icon)

        header = QLabel('Add New Password')
        header.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
        ''')
        title_layout.addWidget(header)
        title_layout.addStretch()
        header_layout.addLayout(title_layout)

        # Description
        description = QLabel(
            "Store your credentials securely in your password manager")
        description.setStyleSheet('''
            font-size: 14px;
            color: #64748b;
            margin-top: 4px;
            margin-left: 40px;
        ''')
        header_layout.addWidget(description)

        main_layout.addWidget(header_container)

        # Content frame with improved styling
        content_frame = QFrame()
        content_frame.setStyleSheet('''
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: none;
            }
        ''')

        # Add shadow effect to content
        content_shadow = QGraphicsDropShadowEffect()
        content_shadow.setBlurRadius(20)
        content_shadow.setColor(QColor(15, 23, 42, 20))
        content_shadow.setOffset(0, 4)
        content_frame.setGraphicsEffect(content_shadow)

        # Create a scroll area with enhanced styling
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet('''
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        ''')
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(24, 24, 24, 24)
        scroll_layout.setSpacing(18)

        # Form section
        form_section = QFrame()
        form_section.setStyleSheet('''
            QFrame {
                background-color: #f1f5f9;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
        ''')

        form_layout = QVBoxLayout(form_section)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(14)

        # Section title with icon
        form_title_layout = QHBoxLayout()
        form_title_icon = QLabel("📝")
        form_title_icon.setStyleSheet('font-size: 16px; color: #475569;')
        form_title_layout.addWidget(form_title_icon)

        form_title = QLabel("Credential Information")
        form_title.setStyleSheet('''
            font-size: 15px;
            font-weight: bold;
            color: #334155;
        ''')
        form_title_layout.addWidget(form_title)
        form_title_layout.addStretch()
        form_layout.addLayout(form_title_layout)

        # Website input - required field with indicator
        website_container = self.create_input_field(
            "🌐", "Website", is_required=True)
        self.website_input = website_container.findChild(QLineEdit)
        form_layout.addWidget(website_container)

        # Username input - required field with indicator
        username_container = self.create_input_field(
            "👤", "Username", is_required=True)
        self.username_input = username_container.findChild(QLineEdit)
        form_layout.addWidget(username_container)

        # Password input - required field with special styling
        password_container = self.create_input_field(
            "🔒", "Password", is_password=True, is_required=True, is_highlighted=True)
        self.password_input = password_container.findChild(QLineEdit)
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_container)

        # URL input
        url_container = self.create_input_field("🔗", "URL")
        self.url_input = url_container.findChild(QLineEdit)
        form_layout.addWidget(url_container)

        # Email input
        email_container = self.create_input_field("✉️", "Email")
        self.email_input = email_container.findChild(QLineEdit)
        form_layout.addWidget(email_container)

        # Additional Info input
        additional_info_container = self.create_input_field(
            "📝", "Additional Info", is_multiline=True)
        self.additional_info_input = additional_info_container.findChild(
            QLineEdit)
        form_layout.addWidget(additional_info_container)

        scroll_layout.addWidget(form_section)

        # Status label for feedback
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('''
            color: #10b981;
            font-weight: 600;
            font-size: 14px;
            padding: 10px;
            background-color: #ecfdf5;
            border-radius: 8px;
            border: 1px solid #a7f3d0;
        ''')
        self.status_label.setVisible(False)
        scroll_layout.addWidget(self.status_label)

        # Action buttons with improved design
        button_section = QVBoxLayout()
        button_section.setSpacing(14)

        # Generate password button with improved styling
        self.generate_btn = QPushButton('Generate Secure Password')
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        self.generate_btn.setStyleSheet('''
            QPushButton {
                background-color: #f1f5f9;
                color: #4f46e5;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 12px 0;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0e7ff;
                border-color: #a5b4fc;
            }
            QPushButton:pressed {
                background-color: #c7d2fe;
            }
        ''')
        self.generate_btn.setMinimumHeight(46)
        self.generate_btn.clicked.connect(self.generate_password)
        button_section.addWidget(self.generate_btn)

        # Bottom action buttons
        bottom_buttons = QHBoxLayout()
        bottom_buttons.setSpacing(14)

        # Add button with primary styling
        self.add_btn = QPushButton('Save Password')
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet('''
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 0;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
            QPushButton:pressed {
                background-color: #4338ca;
            }
            QPushButton:disabled {
                background-color: #c7d2fe;
                color: #eff6ff;
            }
        ''')
        self.add_btn.setMinimumHeight(46)
        self.add_btn.clicked.connect(self.add_password)
        bottom_buttons.addWidget(self.add_btn)

        # Cancel button
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #f1f5f9;
                color: #334155;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 12px 0;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        ''')
        self.cancel_btn.setMinimumHeight(46)
        self.cancel_btn.clicked.connect(self.reject)
        bottom_buttons.addWidget(self.cancel_btn)

        button_section.addLayout(bottom_buttons)

        scroll_layout.addLayout(button_section)
        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(scroll_area)

        main_layout.addWidget(content_frame)

        self.setLayout(main_layout)

    def create_input_field(self, icon_text, label_text, is_password=False, is_multiline=False, is_required=False, is_highlighted=False):
        container = QFrame()

        # Apply different styling if this field is highlighted
        if is_highlighted:
            container.setStyleSheet('''
                background-color: #eff6ff;
                border-radius: 8px;
                border: 1px solid #bfdbfe;
            ''')
        else:
            container.setStyleSheet('''
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            ''')

        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        icon = QLabel(icon_text)
        icon.setFixedWidth(24)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet('font-size: 16px; color: #64748b;')
        layout.addWidget(icon)

        info = QVBoxLayout()
        info.setContentsMargins(0, 0, 0, 0)
        info.setSpacing(3)

        # Label with required indicator if needed
        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(5)

        field_label = QLabel(label_text)
        field_label.setStyleSheet('''
            font-size: 12px;
            color: #64748b;
            font-weight: 500;
        ''')
        label_layout.addWidget(field_label)

        if is_required:
            required_label = QLabel("*")
            required_label.setStyleSheet('''
                font-size: 12px;
                color: #ef4444;
                font-weight: bold;
            ''')
            label_layout.addWidget(required_label)

        label_layout.addStretch()
        info.addLayout(label_layout)

        # Input field
        input_field = QLineEdit()
        if is_multiline:
            input_field.setMinimumHeight(60)

        # Apply different styling if this field is highlighted
        if is_highlighted:
            input_field.setStyleSheet('''
                border: none;
                background-color: transparent;
                font-size: 14px;
                color: #1e40af;
                font-weight: 500;
                padding: 4px 0;
            ''')
        else:
            input_field.setStyleSheet('''
                border: none;
                background-color: transparent;
                font-size: 14px;
                color: #0f172a;
                padding: 4px 0;
            ''')

        info.addWidget(input_field)
        layout.addLayout(info)

        # Add visibility toggle button for password fields
        if is_password:
            toggle_btn = QPushButton()
            toggle_btn.setText("👁️")
            toggle_btn.setToolTip("Show Password")
            toggle_btn.setCursor(Qt.PointingHandCursor)
            toggle_btn.setFixedSize(32, 32)
            toggle_btn.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-color: #f1f5f9;
                    font-size: 14px;
                    color: #6366f1;
                    padding: 4px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    color: #4f46e5;
                    background-color: #e0e7ff;
                }
                QPushButton:pressed {
                    background-color: #c7d2fe;
                }
            ''')
            toggle_btn.clicked.connect(
                lambda: self.toggle_password_visibility(input_field, toggle_btn))
            layout.addWidget(toggle_btn)

        return container

    def toggle_password_visibility(self, password_field, toggle_button):
        if password_field.echoMode() == QLineEdit.Password:
            password_field.setEchoMode(QLineEdit.Normal)
            toggle_button.setText("🔒")
            toggle_button.setToolTip("Hide Password")
        else:
            password_field.setEchoMode(QLineEdit.Password)
            toggle_button.setText("👁️")
            toggle_button.setToolTip("Show Password")

    def show_status_message(self, message, is_error=False):
        if is_error:
            self.status_label.setStyleSheet('''
                color: #dc2626;
                font-weight: 600;
                font-size: 14px;
                padding: 10px;
                background-color: #fef2f2;
                border-radius: 8px;
                border: 1px solid #fecaca;
            ''')
        else:
            self.status_label.setStyleSheet('''
                color: #10b981;
                font-weight: 600;
                font-size: 14px;
                padding: 10px;
                background-color: #ecfdf5;
                border-radius: 8px;
                border: 1px solid #a7f3d0;
            ''')

        self.status_label.setText(message)
        self.status_label.setVisible(True)

        # Hide the message after 3 seconds
        QTimer.singleShot(3000, lambda: self.status_label.setVisible(False))

    def generate_password(self):
        password = generate_password()
        self.password_input.setText(password)
        self.clipboard.copy_to_clipboard(password)
        self.show_status_message(
            "Secure password generated and copied to clipboard")

    def add_password(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        url = self.url_input.text()
        email = self.email_input.text()
        additional_info = self.additional_info_input.text()

        if not all([website, username, password]):
            self.show_status_message(
                "Please fill in all required fields", is_error=True)
            return

        try:
            if self.parent.password_manager.add_password(website, username, password, url, email, additional_info):
                QMessageBox.information(
                    self, 'Success', 'Password added successfully')
                self.accept()
            else:
                self.show_status_message(
                    "Website already exists in your password manager", is_error=True)
        except Exception as e:
            self.show_status_message(
                f"Failed to add password: {str(e)}", is_error=True)
