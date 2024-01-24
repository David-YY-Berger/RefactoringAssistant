import csv
from src import application_properties as ap
from src.gen_files import constants as cons, paths as p, gen_scripts as gs
from src.gen_files.ConsoleHelpers import input_helper as ih
from src.gen_files.enums import Servers
import pandas as pd
import warnings
import random

def write_txt_to_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        file.write(content)


# def run_file(file_rel_path):
#     print("running file " + file_rel_path)
#     exec(open(file_rel_path).read())


def read_lines_as_list_from_file(path, encoding='utf-8'):
    res = []
    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
    for line in lines:
        res.append(line.strip())
    return res


def read_file_as_str(path, encoding='utf-8'):
    try:
        with open(path, 'r', encoding=encoding) as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"The file at {path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_val_from_key_csv(csv_path, key_header, val_header, key):
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[key_header] == key:
                return row[val_header]
    return cons.not_found


def get_server_from_testng(csv_path, testng_file_name, encoding='utf-8'):
    with open(csv_path, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['testngfile'] == testng_file_name:
                return row['server']
    return cons.not_found


def get_sheets_from_excel(excel_file_path):

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        excel_sheets = pd.ExcelFile(excel_file_path)
        return excel_sheets.sheet_names
    print("problem opening the file..")


def read_values_from_sheet_in_excel(excel_file_path, sheet_name):

    row_of_column_header = ap.excel_row_of_column_header
    chosen_column_name = ap.excel_column_with_tests_name
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=row_of_column_header)
        column_list = list(df.columns)
        if chosen_column_name not in column_list:
            print("Couldn't find column called " + chosen_column_name + "!")
            return
        return df[chosen_column_name].tolist()
    print("problem opening the file..")

def read_csv_and_select_section():
    # Step 1: Enter the path to the CSV file
    csv_file_path = input("Enter the path to the CSV file: ")

    # Step 2: Read the CSV file and get the values from the "Section" column
    df = pd.read_csv(csv_file_path)

    # Check if "Section" is a valid header in the CSV
    if "Section" not in df.columns:
        print("Error: 'Section' header not found in the CSV.")
        return

    section_values_set = set(df["Section"].dropna())

    # Step 3: Randomly select a specific section
    random_section = random.choice(list(section_values_set))

    # Step 4: Print only the values in the selected section
    values_in_section = df[df["Section"] == random_section]["Section"].tolist()

    # Print the results
    print(f"All values in the 'Section' column: {section_values_set}")
    print("\nRandomly Selected Section:", random_section)
    print(f"Values in the selected section '{random_section}': {values_in_section}")


# read_csv_and_select_section()



