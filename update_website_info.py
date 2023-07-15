import json
from display_password import display_password
from generate_password import generate_password
from get_password import get_password


def update_website_info():
    with open("passwords.json", "r") as file:
        data = json.load(file)

    website_name = input("Enter the name of the website to update: ")
    found_website = False
    for website in data["passwords"]:
        if website["website"].lower() == website_name.lower():
            found_website = True
            break

    if not found_website:
        print(f"No website found for {website_name}")
        return

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
        website["website"] = new_website_name
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
        website['email'] = new_user_email
    elif choice == '6':
        new_additional_info = input("Enter the new additional information: ")
        website['additional_info'] = new_additional_info

    save_choice = input("Do you want to save the updated information? (y/n): ")
    if save_choice == "y":
        with open('passwords.json', 'w') as file:
            json.dump(data, file)
            print(f"{website_name} informations has been updated.")
            # display the updated information
            display_password(website)
    else:
        update_again_choice = input("Do you want to update again? (y/n): ")
        if update_again_choice == "y":
            update_website_info()
