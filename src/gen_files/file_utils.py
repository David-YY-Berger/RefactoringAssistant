import csv
import os

from src import application_properties as ap
from src.gen_files import constants as cons, paths as p
from src.Classes.test_class import TestAndResult
from src.gen_files.ConsoleHelpers import print_functions as pf
import pandas as pd
import warnings

# openpyxl is needed for exe compilation issues
import openpyxl

workbook = openpyxl.Workbook() # ignore this code, it just explicitly requires openpyxl


def write_txt_to_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        file.write(content)


def append_txt_to_file(path, content, encoding='utf-8'):
    with open(path, 'a', encoding=encoding) as file:
        file.write(content)


def read_lines_as_list_from_file(path, encoding='utf-8'):
    res = []
    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
    for line in lines:
        res.append(line.strip())
    return res


def read_file_content_as_str(path, encoding='utf-8'):
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
            if row[p.testng_header] == testng_file_name:
                return row[p.server_header]
    return cons.not_found


def get_sheets_from_excel(excel_file_path):

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        excel_sheets = pd.ExcelFile(excel_file_path)
        return excel_sheets.sheet_names


def read_test_names_and_results_from_sheet_in_excel(excel_file_path, sheet_name):

    row_of_column_header = ap.excel_row_of_column_header
    test_name_col = ap.excel_column_with_tests_name
    result_col = ap.excel_column_with_result

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=row_of_column_header)
        column_list = list(df.columns)

        if test_name_col not in column_list:
            print("Couldn't find column called '" + test_name_col + "' in sheet " + sheet_name + "!")
            return
        if result_col not in column_list:
            print("Couldn't find column called '" + result_col + "' in sheet " + sheet_name + "!")
            return

        test_and_result_list = []

        for index, row in df.iterrows():
            test_name = row[test_name_col]
            result = row[result_col]
            test_and_result = TestAndResult(test_name, result)
            test_and_result_list.append(test_and_result)

        return test_and_result_list
    # print("problem opening the file..")


def get_sections_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    if ap.csv_column_with_section not in df.columns:
        print("Error: " + ap.csv_column_with_section + " header not found in the CSV.")
        return

    section_values_set = set(df[ap.csv_column_with_section].dropna())
    simplified_section_set = {simplify_section_header(section) for section in section_values_set}
    return list(simplified_section_set)


def read_values_from_section_in_csv(csv_file_path, section_name):
    df = pd.read_csv(csv_file_path)

    df = df[df[ap.csv_column_with_type] == ap.csv_type_value_automated]
    df[ap.csv_column_with_section] = df[ap.csv_column_with_section].apply(simplify_section_header)
    values_in_section = df[df[ap.csv_column_with_section] == section_name][ap.csv_column_with_test_name].tolist()
    return values_in_section


def simplify_section_header(orig_section_header):
    # res = str(orig_section_header).split('>')[0].strip()
    return orig_section_header.replace('Regression - ', '')


def is_excel_file(file_path):
    if not os.path.exists(file_path):
        return False
    _, file_extension = os.path.splitext(file_path)
    excel_extensions = ['.xls', '.xlsx']
    return file_extension.lower() in excel_extensions


def is_csv_file(file_path):
    if not os.path.exists(file_path):
        return False
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.csv'


def is_txt_file(file_path):
    if not os.path.exists(file_path):
        return False
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.txt'

def is_column_headers_exists_in_csv(csv_file_path, required_columns):
    # Read CSV file and check if all required columns exist
    try:
        df = pd.read_csv(csv_file_path)
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            for col in missing_columns:
                print(f"Couldn't find the column header '{col}'. Please ensure that the CSV contains the column header '{col}'.")
            return False
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def is_testrail_csv(file_path):
    return is_csv_file(file_path) and is_column_headers_exists_in_csv(file_path, ap.csv_all_column_headers)


def get_files_from_dir_as_list(directory_path, boolean_function, criteria_expected):
    if not os.path.exists(directory_path):
        return []
    files = os.listdir(directory_path)
    file_paths = []

    for file_name in files:
        file_path = os.path.join(directory_path, file_name)

        if boolean_function:
            if boolean_function(file_path):
                file_paths.append(file_path)
            else:
                pf.print_warning("Discovered - " + file_path + " and found that it is not " + criteria_expected)

    return file_paths