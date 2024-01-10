import csv
from src import constants as cons

def run_file(file_rel_path):
    print("running file " + file_rel_path)
    exec(open(file_rel_path).read())


def write_to_txt_file(path, content):
    with open(path, 'w') as file:
        file.write(content)


def read_lines_as_list_from_file(path):
    res = []
    with open(path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        res.append(line.strip())
    return res


def get_server_from_testng(csv_path, testng_file_name):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['testngfile'] == testng_file_name:
                return row['server']
    return cons.not_found


#
# # Example usage
# csv_file_path = 'data.csv'
# target_x_value = 'b'
# result_y = get_server_from_testng(csv_file_path, target_x_value)
#
# if result_y is not None:
#     print(f"The value of y for x='{target_x_value}' is: {result_y}")
# else:
#     print(f"No entry found for x='{target_x_value}' in the CSV file.")
