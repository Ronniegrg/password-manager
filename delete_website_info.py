import json


def delete_website_info(website_name):
    # Deletes the account, password, URL, and website name from the JSON file
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    passwords = data.get('passwords', [])

    for password in passwords:
        if password['website'] == website_name:
            passwords.remove(password)
            with open('passwords.json', 'w') as file:
                json.dump(data, file)
            return True

    return False
