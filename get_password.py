import json


def get_password(website_name):
    with open('passwords.json') as f:
        data = json.load(f)

    for website in data['passwords']:
        if website['website'].lower() == website_name.lower():
            return {
                'website': website['website'],
                'username': website['username'],
                'password': website['password'],
                'url': website['url'],
                'email': website.get('email', ''),
                'additional_info': website['additional_info']
            }

    return None
