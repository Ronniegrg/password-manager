from terminaltables import SingleTable

from get_all_websites import get_all_websites


def display_websites_table():
    count = 1
    websites = get_all_websites()
    table_data = [["Number", "Website Name"]]
    websites.sort(key=lambda x: x.lower())
    for website in websites:
        table_data.append([count, website])
        count += 1
    table = SingleTable(table_data)
    table.inner_heading_row_border = False
    table.inner_row_border = True
    table.justify_columns = {0: 'left', 1: 'left'}
    table.title = "List of Websites"
    table.title_style = ('', 15, 'bold')
    table.table_style = 'round'
    print(table.table)
