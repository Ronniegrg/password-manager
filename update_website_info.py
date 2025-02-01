import json
from display_password import display_password
from generate_password import generate_password
from get_password import search_and_select


def update_website_info():
    website_info = search_and_select()
    if not website_info:
        print("\nNo website selected")
        return

    with open("passwords.json", "r") as file:
        data = json.load(file)

    for website in data["passwords"]:
        if website["website"].lower() == website_info["website"].lower():
            print("\nWhat would you like to update?")
            print("1. Website name")
            print("2. Username")
            print("3. Password")
            print("4. Website URL")
            print("5. Email Address")
            print("6. Additional Information")
            print("7. Back to main menu")
            choice = input("> ")

            if choice == "7":
                return

            if choice not in ["1", "2", "3", "4", "5", "6"]:
                print("Invalid choice.")
                return

            if choice == "1":
                new_website_name = input("Enter the new website name: ")
                website["website"] = new_website_name
            elif choice == "2":
                new_username = input("Enter the new username: ")
                website["username"] = new_username
            elif choice == "3":
                password_choice = input(
                    "Would you like to generate a new password? (y/n): ").lower()
                # checking if the password_choice is not 'y' or 'n'
                # if not then ask the user to enter the correct choice
                while password_choice not in ['y', 'n']:
                    password_choice = input(
                        "Please enter 'y' for yes and 'n' for no: ").lower()
                if password_choice == "y":
                    password_length = int(
                        input("Enter the desired length of the password: "))
                    new_password = generate_password(password_length)
                    website["password"] = new_password
                    print(f"The new password for {
                          website_info['website']} is: {new_password}")
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
                new_additional_info = input(
                    "Enter the new additional information: ")
                website['additional_info'] = new_additional_info

            save_choice = input(
                "Do you want to save the updated information? (y/n): ")
            while save_choice not in ['y', 'n']:
                save_choice = input(
                    "Please enter 'y' for yes and 'n' for no: ").lower()

            if save_choice == "y":
                with open('passwords.json', 'w') as file:
                    json.dump(data, file)
                print(f"{website['website']} information has been updated.")
                display_password(website)
            else:
                update_again_choice = input(
                    "Do you want to update again? (y/n): ")
                if update_again_choice.lower() == "y":
                    update_website_info()
            break
