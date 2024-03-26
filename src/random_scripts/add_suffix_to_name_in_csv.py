import os
import pandas as pd

import os
import pandas as pd


def add_suffix_to_autotest_names(directory_path, suffix='AT', column='Autotest name'):
    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    # Loop through each CSV file
    for file_name in csv_files:
        file_path = os.path.join(directory_path, file_name)

        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Add suffix 'AT' to the end of every non-NaN value in the 'Autotest name' column
        df[column] = df[column].apply(lambda x: str(x) + str(suffix) if pd.notna(x) else x)

        # Write the modified DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

# Example usage:
directory_path = r'Y:\Test Rail\added_AT_to_autotest_name'
add_suffix_to_autotest_names(directory_path, 'AT', 'Autotest name')
