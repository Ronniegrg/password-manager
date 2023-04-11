import json
import random
import string


def generate_password(length):
    # Generates a random password of given length
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def save_password(account, username, generate_password_option, url, website_name, additional_info, user_email):
    # Saves the account, username, password, URL, and website name to a JSON file
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if website_name.lower() in [x['website_name'].lower() for x in data.values()]:
        print("Website name already exists! Please choose a different website name.")
        return

    if generate_password_option == "yes":
        password_length = int(
            input("Enter the desired length of the password: "))
        password = generate_password(password_length)
    else:
        password = input("Enter the password for the website: ")

    data[account] = {"username": username,
                     "password": password,
                     "url": url,
                     "website_name": website_name,
                     "additional_info": additional_info,
                     "user_email": user_email}

    with open('passwords.json', 'w') as file:
        json.dump(data, file)


def get_password(website):
    with open("passwords.json", "r") as file:
        data = json.load(file)
        print(data)  # print contents of the data variable
    try:
        for account, details in data.items():
            if details['website_name'] == website:
                return details['username'], details['password']
        return None, None
    except KeyError:
        return None, None


def get_password(website):
    with open("passwords.json", "r") as file:
        data = json.load(file)
    try:
        for account, details in data.items():
            if details['website_name'].lower() == website.lower():
                return details['username'], details['password'], details['url'], details['user_email'], details['additional_info']
        return None, None, None, None, None
    except KeyError:
        return None, None, None, None, None


def delete_website_info(website_name):
    # Deletes the account, password, URL, and website name from the JSON file
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if website_name in data:
        del data[website_name]
        with open('passwords.json', 'w') as file:
            json.dump(data, file)
        return True
    else:
        return False


def update_website_info():
    with open("passwords.json", "r") as file:
        data = json.load(file)

    website_name = input("Enter the name of the website to update: ")
    found_website = False
    for key in data.keys():
        if key.lower() == website_name.lower():
            website_name = key
            found_website = True
            break

    if not found_website:
        print(f"No website found for {website_name}")
        return

    website = data[website_name]

    print("What would you like to update?")
    print("1. Website name")
    print("2. Username")
    print("3. Password")
    print("4. Website URL")
    print("5. Email Address")
    print("6. Additional Information")
    choice = input("> ")

    if choice == "1":
        new_website_name = input("Enter the new website name: ")
        website["website_name"] = new_website_name
    elif choice == "2":
        new_username = input("Enter the new username: ")
        website["username"] = new_username
    elif choice == "3":
        password_choice = input(
            "Would you like to generate a new password? (y/n): ").lower()
        if password_choice == "y":
            password_length = int(
                input("Enter the desired length of the password: "))
            use_symbols = input(
                "Do you want to include symbols? (y/n): ").lower() == "y"
            new_password = generate_password(password_length, use_symbols)
            website["password"] = new_password
            print(f"The new password for {website_name} is: {new_password}")
        else:
            new_password = input("Enter the new password: ")
            website["password"] = new_password
    elif choice == "4":
        new_website_url = input("Enter the new website URL: ")
        website["url"] = new_website_url
    elif choice == '5':
        new_user_email = input("Enter the new email address: ")
        website['user_email'] = new_user_email
    elif choice == '6':
        new_additional_info = input("Enter the new additional information: ")
        website['additional_info'] = new_additional_info

    with open('passwords.json', 'w') as file:
        json.dump(data, file)
        print(f"{choice} for {website_name} has been updated.")


def get_all_websites():
    with open('passwords.json', 'r') as file:
        data = json.load(file)
    websites = []
    for account, details in data.items():
        if details['website_name'] not in websites:
            websites.append(details['website_name'])
    return websites


def main():
    # Prompts the user for input and saves passwords
    print("Welcome to Password Manager!")
    while True:
        print("What would you like to do?")
        print("1. Retrieve a password")
        print("2. Save a password")
        print("3. Delete information for a website")
        print("4. Update information for a website")
        print("5. Get all websites")
        print("6. Exit")
        choice = input("> ")

        if choice == "2":
            website_name = input("Enter the name of the website: ")
            website_url = input("Enter the URL of the website: ")
            website_username = input("Enter the username for the website: ")
            user_email = input("Enter your email address: ")
            additional_info = input(
                "Enter any additional information about the website:\n")
            generate_password_option = input(
                "Would you like to generate a password? (yes/no): ")
            save_password(website_name, website_username,
                          generate_password_option, website_url, website_name, additional_info, user_email)
        elif choice == "1":
            website_name = input("Enter the name of the website: ")
            website_username, website_password, url, user_email, additional_info = get_password(
                website_name)
            if website_username is None:
                print(f"No details found for {website_name}")
            else:
                print(f"Website Name: {website_name}")
                if url:
                    print(f"Website Address: {url}")
                if website_username:
                    print(f"Username: {website_username}")
                if user_email:
                    print(f"Email Address: {user_email}")
                if website_password:
                    print(f"Password: {website_password}")
                if additional_info:
                    print(f"Additional Information: {additional_info}")
                print()
        elif choice == "3":
            website_name = input("Enter the name of the website to delete: ")
            deleted = delete_website_info(website_name)
            if deleted:
                print(f"Information for {website_name} deleted successfully.")
            else:
                print(f"No information found for {website_name} ")
        elif choice == "4":
            update_website_info()
        elif choice == "5":
            website_names = get_all_websites()
            if website_names:
                count = 1
                print("Website Names: ")
                for name in website_names:
                    print(f"{count} - {name}")
                    count += 1
            else:
                print("No website names found.")
        elif choice == "6":
            print("Exiting Password Manager...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")

        while True:
            continue_choice = input(
                "Do you want to find another website name? (yes/no): ")
            if continue_choice.lower() == "yes":
                break
            elif continue_choice.lower() == "no":
                print("Exiting Password Manager...")
                return
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")


if __name__ == '__main__':
    main()
