"""
Window for listing all saved websites
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class ListWebsitesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Saved Websites')
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Website', 'Username'])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Refresh button
        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.update_table)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)
        self.update_table()

    def update_table(self):
        try:
            websites = self.parent.password_manager.list_websites()
            self.table.setRowCount(len(websites))

            for row, website in enumerate(websites):
                entry = self.parent.password_manager.get_password(website)
                if entry:
                    self.table.setItem(row, 0, QTableWidgetItem(website))
                    self.table.setItem(
                        row, 1, QTableWidgetItem(entry['username']))

            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to load websites: {str(e)}')
