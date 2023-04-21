import json
import os

from display_password import display_password


def save_password(website_name, website_username, website_password, website_url, website_email, additional_info):
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print("Error: passwords.json is empty or contains invalid JSON data.")
                return
    else:
        data = {'passwords': []}

    passwords = data.get('passwords', [])

    if website_name.lower() in [x['website'].lower() for x in passwords]:
        print("The website already exists.")
        return

    new_password = {
        "website": website_name,
        "username": website_username,
        "password": website_password,
        "url": website_url,
        "email": website_email,
        "additional_info": additional_info
    }
    display_password(new_password)
    # ask user if they want to save the password
    savePassword = input("Do you want to save this password? (yes/no): ")
    if savePassword.lower() == "no":
        # if user doesn't want to save the password, give them the option to create a new password
        print("Password not saved.")
    elif savePassword.lower() == "yes":
        passwords.append(new_password)
        print("Password saved successfully.")
        display_password(new_password)

    with open('passwords.json', 'w') as f:
        json.dump(data, f, indent=4)
