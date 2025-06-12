# Password Manager

A secure password manager application built with Python and PyQt5.

## Features

- Secure password storage with encryption
- Password generation
- Easy password retrieval
- Password strength indicator
- Clipboard management
- User-friendly GUI

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

## Running the Application

To run the application, execute:

```bash
python -m password_manager.main
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

## Security Features

- All passwords are encrypted using Fernet symmetric encryption
- Master password is never stored in plain text
- Clipboard is automatically cleared after copying passwords
- Password strength indicator helps create secure passwords

## File Structure

```
password_manager/
├── __init__.py
├── main.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── password_manager.py
│   ├── encryption.py
│   └── database.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── login_window.py
│   ├── setup_window.py
│   ├── add_password_window.py
│   ├── retrieve_password_window.py
│   ├── update_password_window.py
│   ├── delete_password_window.py
│   ├── list_websites_window.py
│   └── widgets/
│       ├── __init__.py
│       ├── password_strength.py
│       └── custom_widgets.py
└── utils/
    ├── __init__.py
    ├── password_generator.py
    └── clipboard_manager.py
```

---

## Prerequisites

- Python 3.x
- PyQt5 (usually included with Python)
  ```bash
  pip install pyqt5
  ```
  If you encounter issues, install PyQt5 via your OS package manager.

---

## Screenshot

![Password Manager GUI Screenshot](screenshot.png)
_Modern, clean, and easy-to-use interface._

---

## Data Storage

All data is stored locally in `passwords.json` with the following structure:

```json
{
  "passwords": [
    {
      "website": "example.com",
      "username": "yourusername",
      "password": "yourpassword",
      "url": "https://example.com/login",
      "email": "you@example.com",
      "additional_info": "Any extra notes."
    }
  ]
}
```

---

## Security

- **Local Storage Only:** All your data is stored locally and never leaves your computer.
- **No Cloud Sync:** For maximum privacy, there is no cloud or remote storage.
- **File Safety:** Protect your `passwords.json` file with OS-level permissions or encryption for extra security.
- **Open Source:** You can review the code for transparency.

---

## Customization

- **UI Customization:** You can change colors, fonts, and layout in `gui.py`.
- **Password Policy:** Adjust password generation rules in `generate_password.py`.
- **Add Features:** The modular codebase makes it easy to add new features or integrations.

---

## Troubleshooting

- **PyQt5 Not Found:**
  Install with `pip install pyqt5` or your OS package manager.
- **Corrupted `passwords.json`:**
  If the file is corrupted, delete or fix it manually. The app will recreate it if missing.
- **App Won't Start:**
  Ensure you are running Python 3 and have all dependencies installed.

---

## FAQ

**Q: Is my data safe?**
A: All data is stored locally. For extra safety, encrypt your `passwords.json` file.

**Q: Can I use this on another computer?**
A: Yes, copy your `passwords.json` file to the new computer.

**Q: Can I add more fields?**
A: Yes, modify the code in `gui.py` and related files to add more fields.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

_Enjoy your secure and modern password manager!_
