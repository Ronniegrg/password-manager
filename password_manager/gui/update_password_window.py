"""
Window for updating passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QHBoxLayout, QListWidget,
                             QListWidgetItem, QGroupBox, QFormLayout)
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
        self.setWindowTitle('Update Info')
        self.setFixedSize(520, 580)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #555;
            }
            QLineEdit, QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                selection-background-color: #0078d7;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0063b1;
            }
            QPushButton:pressed {
                background-color: #004e8c;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 15px;
                font-weight: bold;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header title
        header_label = QLabel("Update Password Information")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-bottom: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Search section
        search_group = QGroupBox("Find Website")
        search_layout = QVBoxLayout()

        search_form = QHBoxLayout()
        self.website_label = QLabel('Search Website:')
        self.website_search_input = QLineEdit()
        self.website_search_input.setPlaceholderText('Type to search websites...')
        self.website_search_input.setStyleSheet("padding-right: 25px;")
        search_form.addWidget(self.website_label)
        search_form.addWidget(self.website_search_input, 1)
        search_layout.addLayout(search_form)

        self.website_list = QListWidget()
        self.website_list.setMaximumHeight(150)
        self.website_list.setStyleSheet("""
            QListWidget::item { 
                padding: 6px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e6f2ff;
                color: #0078d7;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        search_layout.addWidget(self.website_list)
        self.website_list.hide()

        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)

        # Website information section
        info_group = QGroupBox("Website Information")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        # Editable website name
        self.new_website_label = QLabel('Website:')
        self.new_website_input = QLineEdit()
        self.new_website_input.setMinimumHeight(35)
        form_layout.addRow(self.new_website_label, self.new_website_input)

        # Editable username
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setMinimumHeight(35)
        form_layout.addRow(self.username_label, self.username_input)

        # Editable password with buttons
        self.password_label = QLabel('Password:')
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setMinimumHeight(35)
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        self.generate_btn = QPushButton('Generate')
        self.generate_btn.setToolTip('Generate a secure password')
        self.generate_btn.setMinimumHeight(35)
        self.generate_btn.clicked.connect(self.generate_password)

        self.show_hide_btn = QPushButton('Show')
        self.show_hide_btn.setCheckable(True)
        self.show_hide_btn.setToolTip('Show/Hide Password')
        self.show_hide_btn.setMinimumHeight(35)
        self.show_hide_btn.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.show_hide_btn)
        password_container = QVBoxLayout()
        password_container.addLayout(password_layout)
        password_container.addLayout(button_layout)
        form_layout.addRow(self.password_label, password_container)

        # Editable URL
        self.url_label = QLabel('URL:')
        self.url_input = QLineEdit()
        self.url_input.setMinimumHeight(35)
        form_layout.addRow(self.url_label, self.url_input)

        # Editable email
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setMinimumHeight(35)
        form_layout.addRow(self.email_label, self.email_input)

        # Editable additional info
        self.additional_info_label = QLabel('Additional Info:')
        self.additional_info_input = QLineEdit()
        self.additional_info_input.setMinimumHeight(35)
        form_layout.addRow(self.additional_info_label, self.additional_info_input)

        info_group.setLayout(form_layout)
        main_layout.addWidget(info_group)

        # Buttons container
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Cancel button
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ccc;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        # Update Info button
        self.update_btn = QPushButton('Update Info')
        self.update_btn.clicked.connect(self.update_info)
        self.update_btn.setMinimumWidth(120)
        buttons_layout.addWidget(self.update_btn)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.all_websites = self.parent.password_manager.list_websites()
        self.website_search_input.textChanged.connect(self.filter_websites)
        self.website_list.itemClicked.connect(self.select_website)

    def filter_websites(self, text):
        filtered = [
            w for w in self.all_websites if w.lower().startswith(text.lower())]
        self.website_list.clear()
        if filtered and text:
            for w in filtered:
                item = QListWidgetItem(w)
                self.website_list.addItem(item)
            self.website_list.show()
        else:
            self.website_list.hide()

    def select_website(self, item):
        website = item.text()
        self.website_search_input.setText(website)
        self.website_list.hide()
        self.prefill_fields(website)

    def prefill_fields(self, website):
        if not website:
            self.new_website_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            self.url_input.clear()
            self.email_input.clear()
            self.additional_info_input.clear()
            return
        try:
            entry = self.parent.password_manager.get_password(website)
            if entry:
                self.new_website_input.setText(website)
                self.username_input.setText(entry.get('username', ''))
                self.password_input.setText(entry.get('password', ''))
                self.url_input.setText(entry.get('url', ''))
                self.email_input.setText(entry.get('email', ''))
                self.additional_info_input.setText(
                    entry.get('additional_info', ''))
            else:
                self.new_website_input.clear()
                self.username_input.clear()
                self.password_input.clear()
                self.url_input.clear()
                self.email_input.clear()
                self.additional_info_input.clear()
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to retrieve credentials: {str(e)}')

    def update_info(self):
        old_website = self.website_search_input.text()
        new_website = self.new_website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        url = self.url_input.text()
        email = self.email_input.text()
        additional_info = self.additional_info_input.text()

        if not all([old_website, new_website, username, password]):
            QMessageBox.warning(
                self, 'Error', 'Website, username, and password are required.')
            return

        try:
            if self.parent.password_manager.update_entry_full(
                    old_website, new_website, username, password, url, email, additional_info):
                QMessageBox.information(
                    self, 'Success', 'Information updated successfully')
                self.accept()
            else:
                QMessageBox.warning(
                    self, 'Error', 'Failed to update information. The new website name may already exist.')
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to update information: {str(e)}')

    def generate_password(self):
        password = generate_password()
        self.password_input.setText(password)
        self.clipboard.copy_to_clipboard(password)
        QMessageBox.information(
            self, 'Success', 'Password generated and copied to clipboard')

    def toggle_password_visibility(self):
        if self.show_hide_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_hide_btn.setText('Hide')
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_hide_btn.setText('Show')
