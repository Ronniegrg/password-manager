from prettytable import PrettyTable


def display_password(website_info):
    table = PrettyTable()
    table.field_names = ["Field", "Value"]

    if website_info is None:
        print("No details found.")
    else:
        table.add_row(["Website", website_info["website"]])
        table.add_row(["Email", website_info["email"]])
        table.add_row(["Username", website_info["username"]])
        table.add_row(["Password", website_info["password"]])
        table.add_row(["URL", website_info["url"]])
        table.add_row(["Additional Info", website_info["additional_info"]])

        print(table)
