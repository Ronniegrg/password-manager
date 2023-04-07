# password-manager
## Prerequisites
Python 3.x
How to use
Clone this repository or download the password_manager.py file.
Open a terminal and navigate to the directory where the file is located.
## Usage
Run the command python password_manager.py to start the program.
Choose an option from the menu to save, retrieve, update, or delete a password.
Follow the prompts to enter the required information.
Your password and account details will be saved in a JSON file called passwords.json.
Functions
generate_password(length: int) -> str
Generates a random password of given length.

save_password(account: str, username: str, generate_password_option: str, url: str, website_name: str, additional_info: str, user_email: str) -> None
Saves the account, username, password, URL, and website name to a JSON file.

get_password(website: str) -> Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None]]
Retrieves the username, password, URL, email, and additional information for a website.

delete_website_info(website_name: str) -> bool
Deletes the account, password, URL, and website name from the JSON file.

update_website_info() -> None
Updates the website information for an existing entry in the JSON file.

main() -> None
Prompts the user for input and saves, retrieves, updates, or deletes passwords.
