import json


def get_all_websites():
    with open('passwords.json') as json_file:
        data = json.load(json_file)
        websites = []
        for password in data['passwords']:
            websites.append(password['website'])
        return websites
