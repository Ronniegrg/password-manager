# Password Manager

A secure command-line password manager built with Python that helps you store and manage your website credentials locally.

## Features

- Interactive search functionality for all operations
- Secure random password generation
- Store complete website credentials including:
  - Website name
  - Username/Email
  - Password
  - Login URL
  - Additional notes
- View all stored websites in a formatted table
- Easy navigation with "Back to main menu" option everywhere
- Search-based operations for:
  - Password retrieval
  - Credential updates
  - Website deletion

## Prerequisites

- Python 3.x
- Required Python packages:
  ```bash
  pip install prettytable terminaltables
  ```

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/password-manager.git
   ```

2. Navigate to the project directory:
   ```bash
   cd password-manager
   ```

## Usage

1. Start the program:

   ```bash
   python index.py
   ```

2. Main Menu Options:

   - **1. Retrieve a password**

     - Search by typing website name
     - Use arrow keys to navigate results
     - Press Enter to select
     - ESC to return to main menu

   - **2. Save a password**

     - Enter website details
     - Choose to generate secure password or enter manually
     - Add additional information

   - **3. Delete information**

     - Search for website
     - Confirm deletion
     - Option to cancel

   - **4. Update information**

     - Search for website
     - Choose field to update
     - Generate new password if needed

   - **5. Get all websites**

     - View complete list of stored websites

   - **6. Exit**

## Data Storage

All data is stored locally in `passwords.json` with the following structure:
