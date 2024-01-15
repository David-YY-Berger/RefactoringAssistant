import csv

import src.gen_files.enums
from src.gen_files import constants as cons, paths as p, gen_scripts as gs


# def run_file(file_rel_path):
#     print("running file " + file_rel_path)
#     exec(open(file_rel_path).read())


def write_txt_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)


def read_lines_as_list_from_file(path):
    res = []
    with open(path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        res.append(line.strip())
    return res


def read_file_as_str(path):
    try:
        with open(path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"The file at {path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_val_from_key_csv(csv_path, key_header, val_header, key):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[key_header] == key:
                return row[val_header]
    return cons.not_found


# def write_val_to_key_csv(csv_path, key_header, val_header, key, val_to_write):
#     with open(csv_path, 'w') as file:
#         reader = csv.DictReader(file)
#         writer = csv.DictWriter(file)
#         for row in reader:
#             if row[key_header] == key:
#                 writer.writerow({key_header:key, val_header:val_to_write})
#     print(cons.not_found)


def get_server_from_testng(csv_path, testng_file_name):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['testngfile'] == testng_file_name:
                return row['server']
    # if code got here, we did not find testng file..
    print("Please add the testng file: " + testng_file_name + "\n" +
          "to csv file: " + p.testng_server_csv_path + "\n" 
          "Also, add the server. Use these server names: " + gs.open_list_as_string(list(s.name for s in
                                                                                         src.gen_files.enums.Servers), ", ")
          + "\n")
    return cons.not_found



