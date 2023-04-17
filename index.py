from delete_website_info import delete_website_info
from display_password import display_password
from display_websites_table import display_websites_table
from generate_password import generate_password
from get_password import get_password
from save_password import save_password
from update_website_info import update_website_info


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
            if generate_password_option == "yes":
                # ask user for password length
                password_length = int(
                    input("Enter the length of the password: "))
                input_password = generate_password(password_length)
            else:
                input_password = input("Enter a password: ")
            save_password(website_name, website_username,
                          input_password, website_url, user_email, additional_info)
        elif choice == "1":
            website_name = input("Enter the name of the website: ")
            website_info = get_password(website_name)
            if website_info is None:
                print(f"No details found for {website_name}")
            else:
                display_password(website_info)
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
            display_websites_table()
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
