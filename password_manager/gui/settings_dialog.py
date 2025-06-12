from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QHBoxLayout, QFrame, QTabWidget,
                             QGridLayout, QCheckBox, QComboBox, QSpinBox,
                             QGroupBox, QFontComboBox, QColorDialog, QFormLayout,
                             QRadioButton, QButtonGroup, QScrollArea, QWidget,
                             QFileDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor
import sys
import json
import os
import shutil
from datetime import datetime
if sys.platform == "win32":
    import winreg


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Settings')
        self.setMinimumSize(600, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QTabWidget::pane {
                border: 1px solid #dfe4ea;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e9edf2;
                color: #5c6778;
                min-width: 100px;
                padding: 10px 15px;
                margin-right: 2px;
                border: 1px solid #dfe4ea;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #2c3e50;
                font-weight: bold;
            }
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QPushButton#secondaryButton {
                background-color: #f1f2f6;
                color: #2c3e50;
                border: 1px solid #dfe4ea;
            }
            QPushButton#secondaryButton:hover {
                background-color: #e9edf2;
            }
            QPushButton#destructiveButton {
                background-color: #e74c3c;
            }
            QPushButton#destructiveButton:hover {
                background-color: #c0392b;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dfe4ea;
                border-radius: 5px;
                margin-top: 15px;
                padding-top: 22px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: #34495e;
            }
            QLineEdit, QComboBox, QSpinBox {
                border: 1px solid #dfe4ea;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #3498db;
            }
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)

        self.init_ui()
        self.load_current_settings()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header with icon and title
        header_layout = QHBoxLayout()

        # Settings icon
        icon_label = QLabel()
        if QPixmap('settings.png').isNull() == False:
            pixmap = QPixmap('settings.png').scaled(
                32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)

        # Settings title
        title = QLabel('Settings')
        title.setStyleSheet(
            'font-size: 22px; font-weight: bold; color: #2c3e50;')

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Tab widget for different settings categories
        self.tabs = QTabWidget()

        # Security tab
        security_tab = QWidget()
        security_layout = QVBoxLayout(security_tab)
        security_layout.setContentsMargins(20, 20, 20, 20)
        security_layout.setSpacing(15)

        # Master password section
        password_group = QGroupBox("Master Password")
        password_layout = QVBoxLayout(password_group)

        password_info = QLabel(
            "Your master password protects all your stored passwords. Make sure it's strong and unique.")
        password_info.setWordWrap(True)
        password_info.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")

        self.change_pw_btn = QPushButton('Change Master Password')
        self.change_pw_btn.setIcon(QIcon('settings.png'))
        self.change_pw_btn.setIconSize(QSize(18, 18))
        self.change_pw_btn.clicked.connect(self.open_change_password_dialog)

        password_layout.addWidget(password_info)
        password_layout.addWidget(self.change_pw_btn)

        # Session security
        session_group = QGroupBox("Session Security")
        session_layout = QVBoxLayout(session_group)

        auto_lock_layout = QHBoxLayout()
        auto_lock_label = QLabel("Auto-lock after inactivity:")
        self.auto_lock_combo = QComboBox()
        self.auto_lock_combo.addItems(
            ["Never", "5 minutes", "15 minutes", "30 minutes", "1 hour"])
        auto_lock_layout.addWidget(auto_lock_label)
        auto_lock_layout.addWidget(self.auto_lock_combo, 1)

        self.lock_on_exit = QCheckBox("Lock vault when application is closed")
        self.lock_on_exit.setChecked(True)

        session_layout.addLayout(auto_lock_layout)
        session_layout.addWidget(self.lock_on_exit)

        # Add groups to the security tab
        security_layout.addWidget(password_group)
        security_layout.addWidget(session_group)
        security_layout.addStretch()

        # Appearance tab
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout(appearance_tab)
        appearance_layout.setContentsMargins(20, 20, 20, 20)
        appearance_layout.setSpacing(15)

        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout(theme_group)

        self.light_theme = QRadioButton("Light")
        self.dark_theme = QRadioButton("Dark")
        self.system_theme = QRadioButton("Use system setting")
        self.light_theme.setChecked(True)

        theme_layout.addWidget(self.light_theme)
        theme_layout.addWidget(self.dark_theme)
        theme_layout.addWidget(self.system_theme)

        font_group = QGroupBox("Font")
        font_layout = QGridLayout(font_group)

        font_label = QLabel("Application Font:")
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Segoe UI"))

        font_size_label = QLabel("Font Size:")
        self.font_size = QSpinBox()
        self.font_size.setMinimum(8)
        self.font_size.setMaximum(16)
        self.font_size.setValue(10)

        font_layout.addWidget(font_label, 0, 0)
        font_layout.addWidget(self.font_combo, 0, 1)
        font_layout.addWidget(font_size_label, 1, 0)
        font_layout.addWidget(self.font_size, 1, 1)

        appearance_layout.addWidget(theme_group)
        appearance_layout.addWidget(font_group)
        appearance_layout.addStretch()

        # Advanced tab
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab)
        advanced_layout.setContentsMargins(20, 20, 20, 20)
        advanced_layout.setSpacing(15)

        data_group = QGroupBox("Data Management")
        data_layout = QVBoxLayout(data_group)

        backup_btn = QPushButton("Export Data Backup")
        backup_btn.setObjectName("secondaryButton")
        backup_btn.setIcon(QIcon('settings.png'))
        backup_btn.setIconSize(QSize(18, 18))
        backup_btn.clicked.connect(self.export_backup)

        restore_btn = QPushButton("Import from Backup")
        restore_btn.setObjectName("secondaryButton")
        restore_btn.setIcon(QIcon('settings.png'))
        restore_btn.setIconSize(QSize(18, 18))
        restore_btn.clicked.connect(self.import_backup)

        clear_btn = QPushButton("Clear All Data")
        clear_btn.setObjectName("destructiveButton")
        clear_btn.setIcon(QIcon('settings.png'))
        clear_btn.setIconSize(QSize(18, 18))

        data_layout.addWidget(backup_btn)
        data_layout.addWidget(restore_btn)
        data_layout.addWidget(clear_btn)

        advanced_layout.addWidget(data_group)
        advanced_layout.addStretch()

        # Add all tabs
        self.tabs.addTab(security_tab, "Security")
        self.tabs.addTab(appearance_tab, "Appearance")
        self.tabs.addTab(advanced_tab, "Advanced")

        main_layout.addWidget(self.tabs)

        # Footer with buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton('Save Changes')
        self.save_btn.clicked.connect(self.save_settings)

        self.reset_btn = QPushButton('Reset to Defaults')
        self.reset_btn.setObjectName("secondaryButton")
        self.reset_btn.clicked.connect(self.reset_settings)

        self.close_btn = QPushButton('Close')
        self.close_btn.setObjectName("secondaryButton")
        self.close_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        button_layout.addWidget(self.save_btn)

        main_layout.addLayout(button_layout)

    def open_change_password_dialog(self):
        dlg = ChangeMasterPasswordDialog(self.parent)
        dlg.exec_()

    def save_settings(self):
        # Save security settings
        auto_lock_time = self.auto_lock_combo.currentText()
        lock_on_exit = self.lock_on_exit.isChecked()

        # Convert auto_lock_time to seconds for storage
        auto_lock_seconds = 0  # Default to never
        if auto_lock_time == "5 minutes":
            auto_lock_seconds = 5 * 60
        elif auto_lock_time == "15 minutes":
            auto_lock_seconds = 15 * 60
        elif auto_lock_time == "30 minutes":
            auto_lock_seconds = 30 * 60
        elif auto_lock_time == "1 hour":
            auto_lock_seconds = 60 * 60

        # Save appearance settings
        if self.light_theme.isChecked():
            theme = "light"
        elif self.dark_theme.isChecked():
            theme = "dark"
        else:
            theme = "system"

        font_family = self.font_combo.currentFont().family()
        font_size = self.font_size.value()

        # Save all settings to the settings manager
        from password_manager.config.settings import Settings
        settings = Settings()

        # Security settings
        settings.set("auto_lock_timeout", auto_lock_seconds)
        settings.set("lock_on_exit", lock_on_exit)

        # Appearance settings
        settings.set("theme", theme)
        settings.set("font_family", font_family)
        settings.set("font_size", font_size)

        # Apply the appearance changes to the current application
        self.apply_appearance_settings(theme, font_family, font_size)

        QMessageBox.information(self, "Settings Saved",
                                "Your settings have been saved successfully.")
        self.accept()

    def apply_appearance_settings(self, theme, font_family, font_size):
        """Apply the appearance settings to the current application."""
        app_font = QFont(font_family, font_size)
        self.parent.setFont(app_font)
        if theme == "light":
            self.apply_light_theme()
        elif theme == "dark":
            self.apply_dark_theme()
        elif theme == "system":
            if is_system_dark_mode():
                self.apply_dark_theme()
            else:
                self.apply_light_theme()

    def apply_light_theme(self):
        """Apply light theme to the application."""
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

        self.parent.setPalette(light_palette)

    def apply_dark_theme(self):
        """Apply dark theme to the application."""
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

        self.parent.setPalette(dark_palette)

        # Apply dark theme CSS to main window and all child widgets
        self.parent.setStyleSheet('''
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
            QPushButton#secondaryButton {
                background-color: #2d3436;
                color: #dcdde1;
                border: 1px solid #3f4a56;
            }
            QPushButton#secondaryButton:hover {
                background-color: #3f4a56;
            }
            QLineEdit, QComboBox, QSpinBox, QFontComboBox {
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
            QTabWidget::pane {
                border: 1px solid #3f4a56;
                background-color: #2d3436;
            }
            QTabBar::tab {
                background-color: #1e272e;
                color: #95a5a6;
                border: 1px solid #3f4a56;
            }
            QTabBar::tab:selected {
                background-color: #2d3436;
                color: #dcdde1;
            }
            QGroupBox {
                border: 1px solid #3f4a56;
                color: #dcdde1;
            }
            QGroupBox::title {
                color: #dcdde1;
            }
            QRadioButton {
                color: #dcdde1;
            }
            QCheckBox {
                color: #dcdde1;
            }
            QDialog {
                background-color: #1e272e;
            }
            QScrollArea {
                background-color: #1e272e;
            }
            QScrollBar {
                background-color: #2d3436;
            }
        ''')

    def reset_settings(self):
        reply = QMessageBox.question(self, 'Reset Settings',
                                     'Are you sure you want to reset all settings to default values?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Reset form controls to default values
            self.auto_lock_combo.setCurrentText("15 minutes")
            self.lock_on_exit.setChecked(True)
            self.light_theme.setChecked(True)
            self.font_combo.setCurrentFont(QFont("Segoe UI"))
            self.font_size.setValue(10)

            # Reset settings in the settings manager
            from password_manager.config.settings import Settings
            settings = Settings()
            settings.set("auto_lock_timeout", 15 * 60)  # 15 minutes
            settings.set("lock_on_exit", True)
            settings.set("theme", "light")
            settings.set("font_family", "Segoe UI")
            settings.set("font_size", 10)

            # Reapply the appearance settings
            self.apply_appearance_settings("light", "Segoe UI", 10)

            QMessageBox.information(self, "Settings Reset",
                                    "All settings have been reset to default values.")
            self.accept()

    def load_current_settings(self):
        """Load the current settings from the settings manager and update the UI."""
        from password_manager.config.settings import Settings
        settings = Settings()
        auto_lock_seconds = settings.get("auto_lock_timeout", 15 * 60)
        lock_on_exit = settings.get("lock_on_exit", True)
        if auto_lock_seconds == 0:
            self.auto_lock_combo.setCurrentText("Never")
        elif auto_lock_seconds == 5 * 60:
            self.auto_lock_combo.setCurrentText("5 minutes")
        elif auto_lock_seconds == 15 * 60:
            self.auto_lock_combo.setCurrentText("15 minutes")
        elif auto_lock_seconds == 30 * 60:
            self.auto_lock_combo.setCurrentText("30 minutes")
        elif auto_lock_seconds == 60 * 60:
            self.auto_lock_combo.setCurrentText("1 hour")
        self.lock_on_exit.setChecked(lock_on_exit)
        theme = settings.get("theme", "light")
        font_family = settings.get("font_family", "Segoe UI")
        font_size = settings.get("font_size", 10)
        if theme == "light":
            self.light_theme.setChecked(True)
        elif theme == "dark":
            self.dark_theme.setChecked(True)
        else:
            self.system_theme.setChecked(True)
        self.font_combo.setCurrentFont(QFont(font_family))
        self.font_size.setValue(font_size)
        # Apply the theme immediately to the dialog as well
        if theme == "system":
            if is_system_dark_mode():
                self.apply_dark_theme()
            else:
                self.apply_light_theme()
        elif theme == "dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def export_backup(self):
        """Export the current database as a backup file"""
        try:
            # Get the database file path from the parent window
            db_file = os.path.join(
                os.getcwd(), self.parent.password_manager.db.db_file)
            print(f"Database file path: {db_file}")  # Debug print

            if not os.path.exists(db_file):
                QMessageBox.critical(
                    self, "Error", f"Database file not found at: {db_file}")
                return

            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"password_manager_backup_{timestamp}.json"

            # Open file dialog for saving backup
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Backup",
                default_name,
                "JSON Files (*.json)"
            )

            if file_path:
                # Copy the database file to the selected location
                shutil.copy2(db_file, file_path)
                QMessageBox.information(
                    self,
                    "Success",
                    f"Backup successfully exported to:\n{file_path}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export backup:\n{str(e)}\n\nDatabase path: {db_file}"
            )

    def import_backup(self):
        """Import a backup file to restore the database"""
        try:
            # Open file dialog for selecting backup file
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Backup",
                "",
                "JSON Files (*.json)"
            )

            if not file_path:
                return

            # Verify the backup file is valid JSON
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Invalid backup file: Not a valid JSON file"
                )
                return

            # Confirm with user
            reply = QMessageBox.warning(
                self,
                "Confirm Import",
                "This will replace your current database with the backup.\n"
                "Are you sure you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Get the database file path from the parent window
                db_file = os.path.join(
                    os.getcwd(), self.parent.password_manager.db.db_file)
                print(f"Database file path: {db_file}")  # Debug print

                # Create a backup of current database before importing
                if os.path.exists(db_file):
                    backup_name = f"{db_file}.pre_import_backup"
                    shutil.copy2(db_file, backup_name)

                # Copy the backup file to the database location
                shutil.copy2(file_path, db_file)

                # Reload the database
                self.parent.password_manager.db.load_database()

                QMessageBox.information(
                    self,
                    "Success",
                    "Backup successfully imported.\n"
                    "The application will now use the restored data."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to import backup:\n{str(e)}\n\nDatabase path: {db_file}"
            )


class ChangeMasterPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Change Master Password')
        self.setMinimumSize(450, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit {
                border: 1px solid #dfe4ea;
                border-radius: 4px;
                padding: 10px;
                background-color: white;
                margin-bottom: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QPushButton#secondaryButton {
                background-color: #f1f2f6;
                color: #2c3e50;
                border: 1px solid #dfe4ea;
            }
            QPushButton#secondaryButton:hover {
                background-color: #e9edf2;
            }
            .passwordStrengthWeak {
                color: #e74c3c;
            }
            .passwordStrengthMedium {
                color: #f39c12;
            }
            .passwordStrengthStrong {
                color: #2ecc71;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        # Header with icon and title
        header_layout = QHBoxLayout()

        # Lock icon (using settings.png as a placeholder - you may want to add a lock icon)
        icon_label = QLabel()
        if QPixmap('settings.png').isNull() == False:
            pixmap = QPixmap('settings.png').scaled(
                28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)

        # Title
        section_label = QLabel('Change Master Password')
        section_label.setStyleSheet(
            'font-size: 20px; font-weight: bold; color: #2c3e50; margin-left: 10px;')

        header_layout.addWidget(icon_label)
        header_layout.addWidget(section_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Description
        description = QLabel(
            "Your master password is used to encrypt and protect all your stored passwords. Make sure to choose a strong password that you can remember.")
        description.setWordWrap(True)
        description.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(description)

        # Add a separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #dfe6e9;")
        layout.addWidget(line)

        # Form content in a form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 10, 0, 10)

        # Current password
        current_label = QLabel('Current Password:')
        self.current_input = QLineEdit()
        self.current_input.setEchoMode(QLineEdit.Password)
        self.current_input.setPlaceholderText(
            "Enter your current master password")
        form_layout.addRow(current_label, self.current_input)

        # Add some space
        spacer = QLabel("")
        spacer.setMinimumHeight(10)
        form_layout.addRow(spacer)

        # New password
        new_label = QLabel('New Password:')
        self.new_input = QLineEdit()
        self.new_input.setEchoMode(QLineEdit.Password)
        self.new_input.setPlaceholderText("Enter a strong new password")
        self.new_input.textChanged.connect(self.check_password_strength)
        form_layout.addRow(new_label, self.new_input)

        # Password strength indicator
        self.strength_label = QLabel("")
        self.strength_label.setStyleSheet("margin-top: -5px;")
        form_layout.addRow("", self.strength_label)

        # Confirm new password
        confirm_label = QLabel('Confirm New Password:')
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Confirm your new password")
        self.confirm_input.textChanged.connect(self.check_passwords_match)
        form_layout.addRow(confirm_label, self.confirm_input)

        # Password match indicator
        self.match_label = QLabel("")
        self.match_label.setStyleSheet("margin-top: -5px;")
        form_layout.addRow("", self.match_label)

        layout.addLayout(form_layout)

        # Tips for strong passwords
        tips_frame = QFrame()
        tips_frame.setStyleSheet("""
            background-color: #ebf5fb;
            border-radius: 4px;
            padding: 10px;
        """)
        tips_layout = QVBoxLayout(tips_frame)

        tips_header = QLabel("Tips for a strong password:")
        tips_header.setStyleSheet("font-weight: bold; color: #3498db;")

        tips_content = QLabel(
            "• Use at least 12 characters\n• Include uppercase and lowercase letters\n• Add numbers and special characters\n• Avoid common words and patterns")
        tips_content.setStyleSheet("color: #2c3e50;")

        tips_layout.addWidget(tips_header)
        tips_layout.addWidget(tips_content)

        layout.addWidget(tips_frame)
        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setObjectName("secondaryButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton('Change Password')
        self.save_btn.clicked.connect(self.change_master_password)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

    def check_password_strength(self):
        """Check password strength and update the indicator"""
        password = self.new_input.text()

        if not password:
            self.strength_label.setText("")
            return

        # Simple password strength algorithm
        score = 0

        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(not c.isalnum() for c in password):
            score += 1

        if score <= 2:
            self.strength_label.setText("Weak password")
            self.strength_label.setStyleSheet(
                "color: #e74c3c; margin-top: -5px;")
        elif score <= 3:
            self.strength_label.setText("Moderate password")
            self.strength_label.setStyleSheet(
                "color: #f39c12; margin-top: -5px;")
        else:
            self.strength_label.setText("Strong password")
            self.strength_label.setStyleSheet(
                "color: #2ecc71; margin-top: -5px;")

    def check_passwords_match(self):
        """Check if passwords match and update the indicator"""
        if not self.new_input.text() or not self.confirm_input.text():
            self.match_label.setText("")
            return

        if self.new_input.text() == self.confirm_input.text():
            self.match_label.setText("Passwords match")
            self.match_label.setStyleSheet("color: #2ecc71; margin-top: -5px;")
        else:
            self.match_label.setText("Passwords do not match")
            self.match_label.setStyleSheet("color: #e74c3c; margin-top: -5px;")

    def change_master_password(self):
        current = self.current_input.text()
        new = self.new_input.text()
        confirm = self.confirm_input.text()

        if not current or not new or not confirm:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        if new != confirm:
            QMessageBox.warning(self, 'Error', 'New passwords do not match')
            self.new_input.clear()
            self.confirm_input.clear()
            return

        # Validate current password
        try:
            # Try to re-initialize encryption with the current password
            self.parent.password_manager.encryption.initialize(current)
        except Exception:
            QMessageBox.warning(self, 'Error', 'Current password is incorrect')
            self.current_input.clear()
            return

        # Set new password
        try:
            self.parent.password_manager.encryption.initialize(new)
            self.parent.settings.set('encryption_key', new)
            QMessageBox.information(
                self, 'Success', 'Master password changed successfully!')
            self.accept()
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Failed to change password: {str(e)}')


def is_system_dark_mode():
    if sys.platform != "win32":
        return False  # Default to light on non-Windows
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0  # 0 = dark, 1 = light
    except Exception:
        return False
