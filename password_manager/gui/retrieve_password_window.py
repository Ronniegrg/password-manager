"""
Window for retrieving passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox, QFrame, QHBoxLayout,
                             QSizePolicy, QGraphicsDropShadowEffect, QScrollArea, QWidget,
                             QToolButton)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont, QFontDatabase
from ..utils.clipboard_manager import ClipboardManager


class RetrievePasswordWindow(QDialog):
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
        self.setWindowTitle('Retrieve Password')
        self.setFixedSize(520, 600)  # Slightly larger for better spacing

        # Set window style with a cleaner look
        self.setStyleSheet('''
            QDialog {
                background-color: #f8fafc;
            }
        ''')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Create header with enhanced shadow effect
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
        header_icon.setText("🔐")
        header_icon.setStyleSheet('font-size: 28px; margin-right: 12px;')
        title_layout.addWidget(header_icon)

        header = QLabel('Retrieve Password')
        header.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
        ''')
        title_layout.addWidget(header)
        title_layout.addStretch()
        header_layout.addLayout(title_layout)

        # Improved description with more details
        description = QLabel(
            "Search for a website and safely retrieve your stored credentials")
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

        # Add refined shadow effect to content
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
        scroll_layout.setSpacing(20)

        # Enhanced search section with modern look
        search_section = QFrame()
        search_section.setStyleSheet('''
            QFrame {
                background-color: #f1f5f9;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
        ''')

        search_section_layout = QVBoxLayout(search_section)
        search_section_layout.setContentsMargins(16, 16, 16, 16)
        search_section_layout.setSpacing(12)

        # Section title with icon
        search_title_layout = QHBoxLayout()
        search_title_icon = QLabel("🔍")
        search_title_icon.setStyleSheet('font-size: 16px; color: #475569;')
        search_title_layout.addWidget(search_title_icon)

        search_title = QLabel("Find Website")
        search_title.setStyleSheet('''
            font-size: 15px;
            font-weight: bold;
            color: #334155;
        ''')
        search_title_layout.addWidget(search_title)
        search_title_layout.addStretch()
        search_section_layout.addLayout(search_title_layout)

        # Website search with improved styling
        search_box = QFrame()
        search_box.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }
        ''')
        search_layout = QHBoxLayout(search_box)
        search_layout.setContentsMargins(12, 0, 12, 0)
        search_layout.setSpacing(8)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet('font-size: 14px; color: #64748b;')
        search_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Type to search websites...')
        self.search_input.setStyleSheet('''
            border: none;
            padding: 12px 0px;
            font-size: 14px;
            background-color: transparent;
        ''')
        search_layout.addWidget(self.search_input)
        search_section_layout.addWidget(search_box)
        self.search_input.textChanged.connect(self.filter_websites)

        # Website selection with improved combo box style
        website_select_label = QLabel('Select from available websites:')
        website_select_label.setStyleSheet('''
            font-size: 13px;
            color: #64748b;
            margin-top: 4px;
        ''')
        search_section_layout.addWidget(website_select_label)

        self.website_combo = QComboBox()
        self.website_combo.setMaxVisibleItems(15)
        self.website_combo.setStyleSheet('''
            QComboBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 36px 10px 12px;
                background-color: white;
                font-size: 14px;
                color: #334155;
                selection-background-color: #e2e8f0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: 30px;
                border-left: none;
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
                image: url(down-arrow.png);
            }
            QComboBox QAbstractItemView {
                border: 1px solid #e2e8f0;
                border-radius: 5px;
                selection-background-color: #e2e8f0;
                background-color: white;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 24px;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e2e8f0;
                color: #334155;
            }
        ''')
        self.all_websites = []  # Store all websites for filtering
        self.update_website_list()
        search_section_layout.addWidget(self.website_combo)

        scroll_layout.addWidget(search_section)

        # Credentials section with enhanced visual design
        cred_section = QFrame()
        cred_section.setStyleSheet('''
            QFrame {
                background-color: #f1f5f9;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
        ''')
        cred_layout = QVBoxLayout(cred_section)
        cred_layout.setContentsMargins(16, 16, 16, 16)
        cred_layout.setSpacing(14)

        # Section title with icon
        cred_title_layout = QHBoxLayout()
        cred_title_icon = QLabel("🔒")
        cred_title_icon.setStyleSheet('font-size: 16px; color: #475569;')
        cred_title_layout.addWidget(cred_title_icon)

        cred_title = QLabel("Stored Information")
        cred_title.setStyleSheet('''
            font-size: 15px;
            font-weight: bold;
            color: #334155;
        ''')
        cred_title_layout.addWidget(cred_title)
        cred_title_layout.addStretch()
        cred_layout.addLayout(cred_title_layout)

        # Website name field
        website_name_container = self.create_info_field("🌐", "Website Name")
        self.website_name_display = website_name_container.findChild(QLineEdit)
        cred_layout.addWidget(website_name_container)

        # Username field
        username_container = self.create_info_field("👤", "Username")
        self.username_display = username_container.findChild(QLineEdit)
        cred_layout.addWidget(username_container)

        # Password field with visual emphasis
        password_container = self.create_info_field(
            "🔒", "Password", is_password=True, is_highlighted=True)
        self.password_display = password_container.findChild(QLineEdit)
        self.password_display.setEchoMode(QLineEdit.Password)
        cred_layout.addWidget(password_container)

        # URL field
        url_container = self.create_info_field("🔗", "URL")
        self.url_display = url_container.findChild(QLineEdit)
        cred_layout.addWidget(url_container)

        # Email field
        email_container = self.create_info_field("✉️", "Email")
        self.email_display = email_container.findChild(QLineEdit)
        cred_layout.addWidget(email_container)

        # Additional info field
        additional_info_container = self.create_info_field(
            "📝", "Additional Info", is_multiline=True)
        self.additional_info_display = additional_info_container.findChild(
            QLineEdit)
        cred_layout.addWidget(additional_info_container)

        scroll_layout.addWidget(cred_section)

        # Status label with improved visual feedback
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('''
            color: #10b981;
            font-weight: 500;
            font-size: 13px;
            padding: 8px 0;
            background-color: #ecfdf5;
            border-radius: 6px;
        ''')
        self.status_label.setVisible(False)
        scroll_layout.addWidget(self.status_label)

        # Action buttons with improved design
        button_layout = QHBoxLayout()
        button_layout.setSpacing(14)

        self.copy_btn = QPushButton('Copy Password')
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.setStyleSheet('''
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
        self.copy_btn.setMinimumHeight(46)
        self.copy_btn.clicked.connect(self.copy_password)
        button_layout.addWidget(self.copy_btn)

        self.close_btn = QPushButton('Close')
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet('''
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
        self.close_btn.setMinimumHeight(46)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        scroll_layout.addLayout(button_layout)
        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(scroll_area)

        main_layout.addWidget(content_frame)

        # Connect website selection change
        self.website_combo.currentTextChanged.connect(self.update_credentials)

        self.setLayout(main_layout)

    def create_info_field(self, icon_text, label_text, is_password=False, is_multiline=False, is_highlighted=False):
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

        label = QLabel(label_text)
        label.setStyleSheet('''
            font-size: 12px;
            color: #64748b;
            font-weight: 500;
        ''')
        info.addWidget(label)

        display = QLineEdit()
        if is_multiline:
            display.setMinimumHeight(60)
        display.setReadOnly(True)

        # Apply different styling if this field is highlighted
        if is_highlighted:
            display.setStyleSheet('''
                border: none;
                background-color: transparent;
                font-size: 15px;
                color: #1e40af;
                font-weight: 600;
                padding: 0;
            ''')
        else:
            display.setStyleSheet('''
                border: none;
                background-color: transparent;
                font-size: 14px;
                color: #0f172a;
                font-weight: 500;
                padding: 0;
            ''')

        info.addWidget(display)
        layout.addLayout(info)

        # Add copy button with improved styling
        copy_btn = QPushButton()
        # Use an icon if available
        copy_btn.setIcon(QIcon("clipboard-icon.png"))
        copy_btn.setText("📋")  # Fallback to emoji if icon not available
        copy_btn.setToolTip(f"Copy {label_text}")
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setFixedSize(32, 32)
        copy_btn.setStyleSheet('''
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

        # Connect the button's clicked signal
        copy_btn.clicked.connect(
            lambda: self.copy_field_value(display.text(), label_text))
        layout.addWidget(copy_btn)

        # Add visibility toggle button with improved styling
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
            toggle_btn.clicked.connect(self.toggle_password_visibility)
            layout.addWidget(toggle_btn)

        return container

    def update_website_list(self):
        self.website_combo.clear()
        self.all_websites = self.parent.password_manager.list_websites()
        self.website_combo.addItems(self.all_websites)

    def filter_websites(self, text):
        if not text:
            self.website_combo.clear()
            self.website_combo.addItems(self.all_websites)
            return

        # Filter websites based on the search text (more flexible search)
        filtered = [
            w for w in self.all_websites if text.lower() in w.lower()]
        self.website_combo.clear()
        self.website_combo.addItems(filtered)
        # Auto-select the first filtered result
        if filtered:
            self.website_combo.setCurrentIndex(0)
            self.update_credentials(self.website_combo.currentText())
        else:
            self.clear_all_fields()

    def clear_all_fields(self):
        self.website_name_display.clear()
        self.username_display.clear()
        self.password_display.clear()
        self.url_display.clear()
        self.email_display.clear()
        self.additional_info_display.clear()

    def update_credentials(self, website):
        if not website:
            self.clear_all_fields()
            return

        try:
            entry = self.parent.password_manager.get_password(website)
            if entry:
                self.website_name_display.setText(website)
                self.username_display.setText(entry.get('username', ''))
                self.password_display.setText(entry.get('password', ''))
                self.url_display.setText(entry.get('url', ''))
                self.email_display.setText(entry.get('email', ''))
                self.additional_info_display.setText(
                    entry.get('additional_info', ''))
            else:
                self.clear_all_fields()
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to retrieve credentials: {str(e)}')
            self.clear_all_fields()

    def copy_field_value(self, value, field_name):
        if value:
            self.clipboard.copy_to_clipboard(value)
            self.show_status_message(f"{field_name} copied to clipboard!")
        else:
            QMessageBox.warning(self, 'Nothing to Copy',
                                f'No {field_name.lower()} available to copy.')

    def copy_password(self):
        self.copy_field_value(self.password_display.text(), "Password")

    def show_status_message(self, message):
        self.status_label.setText(message)
        self.status_label.setVisible(True)

        # Create a more prominent visual feedback
        self.status_label.setStyleSheet('''
            color: #10b981;
            font-weight: 600;
            font-size: 14px;
            padding: 10px;
            background-color: #ecfdf5;
            border-radius: 8px;
            border: 1px solid #a7f3d0;
        ''')

        # Hide the message after 3 seconds with animation
        QTimer.singleShot(3000, self.hide_status_message)

    def hide_status_message(self):
        # Create a fade-out effect
        self.status_label.setStyleSheet('''
            color: transparent;
            font-weight: 600;
            font-size: 14px;
            padding: 10px;
            background-color: transparent;
            border-radius: 8px;
            border: 1px solid transparent;
        ''')
        QTimer.singleShot(500, lambda: self.status_label.setVisible(False))

    def toggle_password_visibility(self):
        if self.password_display.echoMode() == QLineEdit.Password:
            self.password_display.setEchoMode(QLineEdit.Normal)
            # Update all toggle buttons that might be for password fields
            for button in self.findChildren(QPushButton):
                if button.toolTip() == "Show Password":
                    button.setText("🔒")
                    button.setToolTip("Hide Password")
        else:
            self.password_display.setEchoMode(QLineEdit.Password)
            # Update all toggle buttons that might be for password fields
            for button in self.findChildren(QPushButton):
                if button.toolTip() == "Hide Password":
                    button.setText("👁️")
                    button.setToolTip("Show Password")
