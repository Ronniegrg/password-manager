"""
Window for listing all saved websites
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QMessageBox, QHBoxLayout, QLineEdit,
                             QLabel, QHeaderView, QMenu, QAction, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor
from .retrieve_password_window import RetrievePasswordWindow


class ListWebsitesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Saved Websites')
        self.setMinimumSize(700, 500)  # Larger minimum size for better usability

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Search section
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to filter websites...")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Add separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # Table section
        table_label = QLabel("Your saved websites:")
        table_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(table_label)

        # Create improved table
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Added a column for actions
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Last Updated'])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)  # Enable sorting
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d4d4d4;
                selection-background-color: #e7f0fd;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #d4d4d4;
                font-weight: bold;
            }
        """)

        # Enable double-click functionality
        self.table.cellDoubleClicked.connect(self.show_website_info)
        # Enable right-click menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        main_layout.addWidget(self.table)

        # Buttons section
        button_layout = QHBoxLayout()

        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.setIcon(QIcon.fromTheme('view-refresh'))
        self.refresh_btn.clicked.connect(self.update_table)

        self.add_new_btn = QPushButton('Add New')
        self.add_new_btn.clicked.connect(self.add_new_password)

        self.view_btn = QPushButton('View Selected')
        self.view_btn.clicked.connect(self.view_selected)

        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.add_new_btn)
        button_layout.addWidget(self.view_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.update_table()

    def update_table(self):
        try:
            websites = self.parent.password_manager.list_websites()
            self.table.setRowCount(len(websites))

            for row, website in enumerate(websites):
                entry = self.parent.password_manager.get_password(website)
                if entry:
                    # Website item
                    website_item = QTableWidgetItem(website)
                    website_item.setData(Qt.UserRole, website)  # Store website name for reference
                    self.table.setItem(row, 0, website_item)

                    # Username item
                    username_item = QTableWidgetItem(entry.get('username', 'N/A'))
                    self.table.setItem(row, 1, username_item)

                    # Last updated (Using placeholder since the original data structure doesn't have this)
                    # In a real implementation, you would store and retrieve actual timestamps
                    last_updated = QTableWidgetItem("N/A")
                    self.table.setItem(row, 2, last_updated)

                    # Apply styling based on complexity or security level
                    if entry.get('password_strength', '').lower() == 'weak':
                        for col in range(3):
                            self.table.item(row, col).setBackground(QColor(255, 200, 200))  # Light red

            # Reset sort indicator to prevent unwanted sorting
            self.table.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)

        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to load websites: {str(e)}')

    def show_website_info(self, row, column):
        website = self.table.item(row, 0).text()
        info_window = RetrievePasswordWindow(self.parent)
        info_window.website_combo.setCurrentText(website)
        info_window.show()

    def filter_table(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            website = self.table.item(row, 0).text().lower()
            username = self.table.item(row, 1).text().lower()

            if search_text in website or search_text in username:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def show_context_menu(self, position):
        menu = QMenu()
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            view_action = QAction("View Details", self)
            view_action.triggered.connect(lambda: self.show_website_info(selected_row, 0))

            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(lambda: self.edit_website_info(selected_row))

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_website(selected_row))

            copy_username_action = QAction("Copy Username", self)
            copy_username_action.triggered.connect(lambda: self.copy_username(selected_row))

            copy_password_action = QAction("Copy Password", self)
            copy_password_action.triggered.connect(lambda: self.copy_password(selected_row))

            menu.addAction(view_action)
            menu.addAction(edit_action)
            menu.addAction(delete_action)
            menu.addSeparator()
            menu.addAction(copy_username_action)
            menu.addAction(copy_password_action)

            menu.exec_(self.table.mapToGlobal(position))

    def edit_website_info(self, row):
        website = self.table.item(row, 0).text()
        if self.parent.update_password_window:
            self.parent.update_password_window.website_combo.setCurrentText(website)
            self.parent.update_password_window.show()

    def delete_website(self, row):
        website = self.table.item(row, 0).text()
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                    f'Are you sure you want to delete "{website}"?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.parent.password_manager.delete_password(website)
                self.update_table()
                QMessageBox.information(self, 'Success', f'"{website}" has been deleted.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to delete website: {str(e)}')

    def copy_username(self, row):
        username = self.table.item(row, 1).text()
        if hasattr(self.parent, 'clipboard_manager'):
            self.parent.clipboard_manager.copy_to_clipboard(username)
            QMessageBox.information(self, 'Success', 'Username copied to clipboard!')

    def copy_password(self, row):
        website = self.table.item(row, 0).text()
        try:
            entry = self.parent.password_manager.get_password(website)
            if entry and 'password' in entry:
                if hasattr(self.parent, 'clipboard_manager'):
                    self.parent.clipboard_manager.copy_to_clipboard(entry['password'])
                    QMessageBox.information(self, 'Success', 'Password copied to clipboard!')
            else:
                QMessageBox.warning(self, 'Error', 'Password not found.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to copy password: {str(e)}')

    def view_selected(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.show_website_info(selected_row, 0)
        else:
            QMessageBox.information(self, 'Information', 'Please select a website first.')

    def add_new_password(self):
        # Open the add password window from the parent
        if hasattr(self.parent, 'show_add_password'):
            self.parent.show_add_password()
        elif hasattr(self.parent, 'add_password_window') and self.parent.add_password_window:
            self.parent.add_password_window.show()
