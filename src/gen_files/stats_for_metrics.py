from enum import Enum, auto

import pandas as pd
from datetime import datetime
import os
from src.gen_files import paths as p


# Define the field names
version_field = 'version'
user_name_field = 'user_name'
date_field = 'date'
time_field = 'time'
product_field = 'product'
is_success_field = 'is_success'
num_files_created_field = 'num_files_created'
missing_files_found_field = 'missing_files_found'
files_added_to_testng_field = 'files_added_to_testng'
error_msg_field = 'error_msg'
tests_analyzed_field = 'test_analyzed'
ng_files_found_field = 'ng_files_found'
non_ng_files_found_field = 'non_ng_files_found'
total_files_with_descrepancies_field = 'total_files_with_descrepancies'
total_files_without_descrepancies_field = 'total_files_without_descrepancies'
passed_tests_with_no_ng_path_field = 'passed_tests_with_no_ng_path'
passed_tests_found_with_no_change_field = 'passed_tests_found_with_no_change'
ng_files_overwritten_field = 'ng_files_overwritten'
files_with_new_descrepencies_field = 'files_with_new_descrepencies'



flag_ignore_david = True


class product_names(Enum):
    Refactor_Tests = auto()
    Test_List_Compare = auto()
    Discrepancy_Tracker = auto()
    Add_Suffix_To_CSV = auto()


# Function to append a row to the CSV file
# BE CAREFUL WITH THE ORDER OF EVERYTHING!!!!
def append_to_stats(version=None, user_name=None, date=None, time=None,
                    product=None, is_success=None, num_files_created=None,
                    missing_files_found=None, files_added_to_testng=None,
                    error_msg=None, tests_analyzed=None, ng_files_found=None,
                    non_ng_files_found=None, total_files_with_descrepancies=None,
                    total_files_without_descrepancies=None,
                    passed_tests_with_no_ng_path=None,
                    passed_tests_found_with_no_change=None,
                    ng_files_overwritten=None,
                    files_with_new_descrepencies=None):

    if user_name == 'davidbe' and flag_ignore_david:
        return
    file_path = p.path_for_stats
    header = [version_field, user_name_field, date_field, time_field,
              product_field, is_success_field, num_files_created_field,
              missing_files_found_field, files_added_to_testng_field,
              error_msg_field, tests_analyzed_field, ng_files_found_field,
              non_ng_files_found_field, total_files_with_descrepancies_field,
              total_files_without_descrepancies_field,
              passed_tests_with_no_ng_path_field,
              passed_tests_found_with_no_change_field,
              ng_files_overwritten_field,
              files_with_new_descrepencies_field]

    try:
        # Create a dictionary with the data
        data = {
            version_field: [version],
            user_name_field: [user_name],
            date_field: [date],
            time_field: [time],
            product_field: [product],
            is_success_field: [is_success],
            num_files_created_field: [num_files_created],
            missing_files_found_field: [missing_files_found],
            files_added_to_testng_field: [files_added_to_testng],
            error_msg_field: [error_msg],
            tests_analyzed_field: [tests_analyzed],
            ng_files_found_field: [ng_files_found],
            non_ng_files_found_field: [non_ng_files_found],
            total_files_with_descrepancies_field: [total_files_with_descrepancies],
            total_files_without_descrepancies_field: [total_files_without_descrepancies],
            passed_tests_with_no_ng_path_field: [passed_tests_with_no_ng_path],
            passed_tests_found_with_no_change_field: [passed_tests_found_with_no_change],
            ng_files_overwritten_field: [ng_files_overwritten],
            files_with_new_descrepencies_field: [files_with_new_descrepencies]
        }

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Check if the CSV file already exists
        if os.path.exists(file_path):
            # If it exists, append the DataFrame to the CSV file without the header
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            # If it doesn't exist, create a new file with the header
            df.to_csv(file_path, index=False)

    except PermissionError:
        # If there's a permission error, create a new file in the same directory with a different name
        new_file_path = os.path.join(p.dir_for_stats, f'{user_name}_temp.csv')

        # Check if the user-specific file already exists
        if os.path.exists(new_file_path):
            # If it exists, append the data to the existing file without the header
            df.to_csv(new_file_path, mode='a', header=False, index=False)
        else:
            # If it doesn't exist, create a new file with the header
            df_header = pd.DataFrame(columns=header)
            df_header.to_csv(new_file_path, index=False)

            # Append the data to the new file
            df.to_csv(new_file_path, mode='a', header=False, index=False)
