import json


def delete_website_info(website_name):
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    passwords = data.get('passwords', [])
    original_length = len(passwords)

    while True:
        print("\nWhat would you like to do?")
        print("1. Delete website information")
        print("2. Cancel deletion")
        print("3. Back to main menu")
        choice = input("> ")

        if choice == "1":
            confirmation = input(f"Are you sure you want to delete {
                                 website_name}? (y/n): ")
            if confirmation.lower() == 'y':
                data['passwords'] = [
                    p for p in passwords if p['website'] != website_name]
                with open('passwords.json', 'w') as file:
                    json.dump(data, file)
                return True
            else:
                print("Deletion cancelled.")
                return False
        elif choice == "2":
            print("Deletion cancelled.")
            return False
        elif choice == "3":
            return False
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
