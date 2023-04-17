import json
import os


def save_password(website_name, website_username, website_password, website_url, website_email, additional_info):
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as f:
            data = json.load(f)
    else:
        data = {'passwords': []}

    passwords = data.get('passwords', [])

    if website_name.lower() in [x['website'].lower() for x in passwords]:
        print("Password for this website already exists.")
        return

    new_password = {
        "website": website_name,
        "username": website_username,
        "password": website_password,
        "url": website_url,
        "email": website_email,
        "additional_info": additional_info
    }

    passwords.append(new_password)

    with open('passwords.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("Password saved successfully.")
