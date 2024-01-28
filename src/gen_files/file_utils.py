import csv
import os

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


def get_sections_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    if ap.csv_section_header not in df.columns:
        print("Error: " + ap.csv_section_header + " header not found in the CSV.")
        return

    section_values_set = set(df[ap.csv_section_header].dropna())
    simplified_section_set = {simplify_section_header(section) for section in section_values_set}
    return list(simplified_section_set)


def read_values_from_section_in_csv(csv_file_path, section_name):
    df = pd.read_csv(csv_file_path)
    df[ap.csv_section_header] = df[ap.csv_section_header].apply(simplify_section_header)
    values_in_section = df[df[ap.csv_section_header] == section_name][ap.csv_column_With_tests_name].tolist()
    return values_in_section


def simplify_section_header(orig_section_header):
    res = str(orig_section_header).split('>')[0].strip()
    return res


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


