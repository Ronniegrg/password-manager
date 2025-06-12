"""
Window for deleting passwords
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QListWidget, QListWidgetItem,
                             QFrame, QSpacerItem, QSizePolicy, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QColor


class DeletePasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        self.setWindowTitle('Delete Password')
        self.setMinimumSize(450, 350)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title section
        title_label = QLabel('Delete Password Entry')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # Website search group
        search_group = QGroupBox("Website Selection")
        search_layout = QVBoxLayout()

        # Website search with icon
        search_layout_h = QHBoxLayout()
        self.website_label = QLabel('Search:')
        self.website_search_input = QLineEdit()
        self.website_search_input.setPlaceholderText(
            'Type to search websites...')
        search_layout_h.addWidget(self.website_label)
        # Give search box more space
        search_layout_h.addWidget(self.website_search_input, 1)
        search_layout.addLayout(search_layout_h)

        # Website list with better styling
        self.website_list = QListWidget()
        self.website_list.setMaximumHeight(150)
        self.website_list.setAlternatingRowColors(True)
        search_layout.addWidget(self.website_list)
        self.website_list.hide()

        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)

        # Account details group
        account_group = QGroupBox("Account Information")
        account_layout = QVBoxLayout()

        # Username display
        username_layout = QHBoxLayout()
        self.username_label = QLabel('Username:')
        self.username_display = QLineEdit()
        self.username_display.setReadOnly(True)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_display)
        account_layout.addLayout(username_layout)

        account_group.setLayout(account_layout)
        main_layout.addWidget(account_group)

        # Spacer to push buttons to bottom
        main_layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Button section
        button_layout = QHBoxLayout()

        # Cancel button
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.reject)

        # Delete button
        self.delete_btn = QPushButton('Delete Password')
        self.delete_btn.setMinimumWidth(150)
        self.delete_btn.clicked.connect(self.delete_password)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.delete_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Data and connections
        self.selected_website = None
        self.all_websites = self.parent.password_manager.list_websites()
        self.website_search_input.textChanged.connect(self.filter_websites)
        self.website_list.itemClicked.connect(self.select_website)

    def setup_styles(self):
        # Style for the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                padding: 5px 15px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                min-height: 25px;
            }
            QListWidget {
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #e7f0fa;
                color: #000000;
            }
        """)

        # Special styling for the delete button to make it stand out
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                font-weight: bold;
                border: 1px solid #e74c3c;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)

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
        self.selected_website = None
        self.username_display.clear()

    def select_website(self, item):
        website = item.text()
        self.website_search_input.setText(website)
        self.website_list.hide()
        self.selected_website = website
        self.update_credentials(website)

    def update_credentials(self, website):
        if not website:
            self.username_display.clear()
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
        website = self.selected_website or self.website_search_input.text()

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
                    self.all_websites = self.parent.password_manager.list_websites()
                    self.website_search_input.clear()
                    self.username_display.clear()
                    self.selected_website = None
                    self.website_list.hide()
                    self.accept()
                else:
                    QMessageBox.warning(
                        self, 'Error', 'Failed to delete password')
            except Exception as e:
                QMessageBox.warning(
                    self, 'Error', f'Failed to delete password: {str(e)}')
