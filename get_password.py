import json
import os
import msvcrt  # Windows-specific keyboard input
from prettytable import PrettyTable


def search_passwords(search_term=""):
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    matches = []
    for entry in data.get('passwords', []):
        if search_term.lower() in entry['website'].lower():
            matches.append(entry)
    return matches


def interactive_search():
    search_term = ""
    selected_index = 0

    while True:
        os.system('cls')  # Clear screen
        print("\nSearch for website (ESC to cancel, Enter to select):")
        print(f"Current search: {search_term}")

        # Show matching results
        matches = search_passwords(search_term)
        if matches:
            table = PrettyTable()
            table.field_names = ["#", "Website", "Username"]
            for i, entry in enumerate(matches, 1):
                table.add_row([i, entry['website'], entry['username']])
            print(table)

        # Get input
        try:
            key = msvcrt.getch()

            # Handle special keys
            if key == b'\r':  # Enter
                return matches[selected_index] if matches else None
            elif key == b'\x1b':  # ESC
                return None
            elif key == b'\x08':  # Backspace
                search_term = search_term[:-1]
            else:
                search_term += key.decode('utf-8')
        except:
            return None


def get_password(website_name):
    """Get password for specified website"""
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for entry in data.get('passwords', []):
        if entry['website'].lower() == website_name.lower():
            return entry
    return None


def search_and_select():
    search_term = ""
    while True:
        os.system('cls')
        print("\nSearch website (Press Enter to select, ESC to return to main menu):")
        print(f"Search: {search_term}")

        matches = []
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
                for entry in data.get('passwords', []):
                    if search_term.lower() in entry['website'].lower():
                        matches.append(entry)

                if search_term and matches:
                    print("\nMatching websites:")
                    for i, entry in enumerate(matches, 1):
                        print(f"{i}. {entry['website']}")

        except (FileNotFoundError, json.JSONDecodeError):
            print("No passwords found")
            return None

        char = msvcrt.getch()
        if char == b'\r' and matches:  # Enter pressed with matches
            while True:
                try:
                    choice = input("\nSelect website number: ")
                    index = int(choice) - 1
                    if 0 <= index < len(matches):
                        return matches[index]  # Return full website entry
                    print("Invalid selection, try again")
                except ValueError:
                    print("Please enter a valid number")
        elif char == b'\x08':  # Backspace
            search_term = search_term[:-1]
        elif char == b'\x1b':  # Escape
            print("\nReturning to main menu...")
            return None
        else:
            try:
                search_term += char.decode('utf-8')
            except:
                continue
