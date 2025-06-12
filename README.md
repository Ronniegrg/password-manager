# Password Manager

A secure password manager application built with Python and PyQt5.

## Features

- Secure password storage with encryption
- Password generation
- Easy password retrieval
- Password strength indicator
- Clipboard management
- User-friendly GUI
- Settings customization

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd password-manager
```

2. Create a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies

- PyQt5 (>=5.15.0): GUI framework
- cryptography (>=3.4.0): For encryption/decryption of passwords
- pyperclip (>=1.8.0): For clipboard operations

## Running the Application

To run the application, execute:

```bash
python gui.py
```

## First Run

On first run, you'll be prompted to:

1. Set up a master password
2. This password will be used to encrypt/decrypt your stored passwords
3. Make sure to remember this password as it cannot be recovered if lost

## Usage

- **Add Password**: Store new website credentials
- **Get Password**: Retrieve stored passwords
- **Update Password**: Modify existing passwords
- **Delete Password**: Remove stored passwords
- **List Websites**: View all stored websites
- **Settings**: Customize application behavior

## Security Features

- All passwords are encrypted using Fernet symmetric encryption
- Master password is never stored in plain text
- Clipboard is automatically cleared after copying passwords
- Password strength indicator helps create secure passwords

## Project Structure

```
password-manager/
├── gui.py                 # Main GUI application
├── config.json           # Application configuration
├── passwords.json        # Encrypted password storage
├── requirements.txt      # Project dependencies
├── settings.png         # Application screenshot
└── password_manager/    # Core application package
```

## Configuration

The application settings can be customized through the settings dialog or by manually editing the `config.json` file.

## Data Storage

Passwords are stored in an encrypted format in the `passwords.json` file. Never edit this file manually as it could corrupt your password database.

## Security

- **Local Storage Only:** All your data is stored locally and never leaves your computer.
- **No Cloud Sync:** For maximum privacy, there is no cloud or remote storage.
- **File Safety:** Protect your `passwords.json` file with OS-level permissions or encryption for extra security.
- **Open Source:** You can review the code for transparency.

## Troubleshooting

- **PyQt5 Not Found:**
  Install with `pip install pyqt5` or your OS package manager.
- **Corrupted `passwords.json`:**
  If the file is corrupted, delete or fix it manually. The app will recreate it if missing.
- **App Won't Start:**
  Ensure you are running Python 3 and have all dependencies installed.

## FAQ

**Q: Is my data safe?**
A: All data is stored locally. For extra safety, encrypt your `passwords.json` file.

**Q: Can I use this on another computer?**
A: Yes, copy your `passwords.json` file to the new computer.

**Q: Can I add more fields?**
A: Yes, modify the code in `gui.py` and related files to add more fields.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

_Enjoy your secure and modern password manager!_
