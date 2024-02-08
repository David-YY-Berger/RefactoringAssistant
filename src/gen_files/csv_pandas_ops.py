import os.path

import pandas as pd
from src.gen_files import paths as p, gen_scripts as gs, constants as cons
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.Classes.test_class import Test


def create_csv_from_test_obj_list(test_obj_list, path):
    df = pd.DataFrame([vars(obj) for obj in test_obj_list])
    df.to_csv(path, index=False)


def create_test_obj_list_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    # Create a list to store Test objects
    test_objects = []

    # Iterate over rows in the DataFrame
    for index, row in df.iterrows():
        # Extract values from the row
        test_name = row[Test.TEST_NAME_FIELD]
        test_path = row[Test.TEST_PATH_FIELD] if Test.TEST_PATH_FIELD in df.columns else ''
        test_section = row[Test.TEST_SECTION_FIELD] if Test.TEST_SECTION_FIELD in df.columns else ''
        test_result = row[Test.TEST_RESULT_FIELD] if Test.TEST_RESULT_FIELD in df.columns else ''
        testng_file_name = row[Test.TESTNG_FILE_NAME_FIELD] if Test.TESTNG_FILE_NAME_FIELD in df.columns else ''

        # Create a Test object and append it to the list
        test_objects.append(Test(test_name, test_path, test_section, test_result, testng_file_name))

    return test_objects


def write_paths_to_test_objs(test_obj_csv_path, test_to_path_csv_path, output_path ='', ignore_warning=False):
    # Read the CSV files

    test_to_paths_df = pd.read_csv(test_to_path_csv_path)
    duplic_in_test_to_path = find_non_unique_values(test_to_path_csv_path, p.test_name_header)
    if len(duplic_in_test_to_path) > 0:
        if not ignore_warning:
            pf.print_warning("Found duplicates test names in project (" + test_to_path_csv_path + '):\n' +
                             gs.open_list_as_string(duplic_in_test_to_path, '\n')
                             + '\n ignoring the duplicates..')
        test_to_paths_df = test_to_paths_df.drop_duplicates(subset=p.test_name_header, keep=False)

    test_objs_df = pd.read_csv(test_obj_csv_path)
    duplic_in_test_obj = find_non_unique_values(test_obj_csv_path, p.test_name_header)
    if len(duplic_in_test_obj) > 0:
        pf.print_warning("Found duplicates in " + test_obj_csv_path + ':\n' +
                         gs.open_list_as_string(duplic_in_test_obj, '\n')
                         + '\n ignoring the duplicates..')
        test_objs_df = test_objs_df.drop_duplicates(subset='test_names', keep=False)

    # Merge the DataFrames on the 'test_name' column
    merged_df = pd.merge(test_objs_df,test_to_paths_df[[p.test_name_header, p.test_path_header]], on=p.test_name_header, how='left')
    # Update 'test_path' column with non-null values from 'test_path_y' column
    merged_df[p.test_path_header] = merged_df[p.test_path_header + '_y'].combine_first(merged_df[p.test_path_header + '_x'])
    # Drop unnecessary columns
    merged_df.drop([p.test_path_header + '_x', p.test_path_header + '_y'], axis=1, inplace=True)
    # Write the updated DataFrame back to CSV
    merged_df.to_csv(output_path, index=False)


def remove_tests_with_no_path(orig_csv_path, output_csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(orig_csv_path)

    # Step 1: Get a list of rows (just the test_name) that do not have a test_path or have '-'
    test_names_without_path = df[df['test_path'].isin([None, '-'])]['test_name'].tolist()

    # Step 2: Remove rows without test_path or containing '-' from the DataFrame
    df = df.dropna(subset=['test_path'])
    df = df[df['test_path'] != '-']

    # Save the updated DataFrame back to a CSV file
    df.to_csv(output_csv_path, index=False)

    pf.print_warning("\nCould not find test_path for these tests (" + str(len(test_names_without_path)) + "):\n" +
                     gs.open_list_as_string(test_names_without_path, "\n"))

    pf.print_warning("Excluded " + str(len(test_names_without_path)) + " tests (without paths) from the analysis"
                   "\nPossible reasons why could not find paths:\n"
                   "\t- Typo in the test name entered (search is Case Sensitive!)\n"
                   "\t- Found more than one file with the name entered (program ignores duplicated)\n"
                   "Please double check the test names entered. You can also try by entering a directory.")
    return df


def find_non_unique_values(csv_path, col_header):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_path)

    # Find and return values that are not unique in the specified column
    non_unique_values = df[df.duplicated(col_header, keep=False)][col_header].tolist()
    return list(set(non_unique_values))


