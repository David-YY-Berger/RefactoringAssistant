from enum import Enum, auto

import pandas as pd
from datetime import datetime
import os


dir_for_stats = r"Y:\QA\Automation\RefactoringAssistant\do_not_delete\dir_for_metric_stats"
path_for_stats = os.path.join(dir_for_stats, 'stats_for_metrics.csv')


# Define the field names
version_field = 'version'
user_name_field = 'user_name'
date_field = 'date'
time_field = 'time'
product_field = 'product'
is_success_field = 'is_success'
num_files_created_field = 'num_files_created'
missing_files_found_field = 'missing_files_found'
discrepancies_found_field = 'discrepancies_found'
files_added_to_testng_field = 'files_added_to_testng'
error_msg_field = 'error_msg'


class product_names(Enum):
    Refactor_Tests = auto()
    Test_List_Compare = auto()



# Function to append a row to the CSV file
def append_to_stats(version=None, user_name=None, date=None, time=None,
                    product=None, is_success=None, num_files_created=None,
                    missing_files_found=None, discrepancies_found=None,
                    files_added_to_testng=None, error_msg=None):
    if user_name == 'davidbe':
        return
    file_path = path_for_stats
    header = [version_field, user_name_field, date_field, time_field,
              product_field, is_success_field, num_files_created_field,
              missing_files_found_field, discrepancies_found_field,
              files_added_to_testng_field, error_msg_field]

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
            discrepancies_found_field: [discrepancies_found],
            files_added_to_testng_field: [files_added_to_testng],
            error_msg_field: [error_msg]
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
        new_file_path = os.path.join(dir_for_stats, f'{user_name}_temp.csv')

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

