import os.path

import pandas as pd
from src.gen_files import paths as p, gen_scripts as gs, constants as cons
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.Classes.test_class import Test
import warnings

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
        test_name = row[Test.TEST_NAME_FIELD] if Test.TEST_NAME_FIELD in df.columns else 'Error didnt find test name column in csv!'
        test_path = row[Test.TEST_PATH_FIELD] if Test.TEST_PATH_FIELD in df.columns else cons.empty_char
        test_section = row[Test.TEST_SECTION_FIELD] if Test.TEST_SECTION_FIELD in df.columns else cons.empty_char
        test_result = row[Test.TEST_RESULT_FIELD] if Test.TEST_RESULT_FIELD in df.columns else cons.empty_char
        testng_file_name = row[Test.TESTNG_FILE_NAME_FIELD] if Test.TESTNG_FILE_NAME_FIELD in df.columns else cons.empty_char
        test_path_ng = row[Test.TEST_PATH_NG_FIELD] if Test.TEST_PATH_NG_FIELD in df.columns else cons.empty_char
        discrepancy = row[Test.DISCREPANCY_FIELD] if Test.DISCREPANCY_FIELD in df.columns else cons.empty_char

        # Create a Test object and append it to the list
        test_objects.append(Test(test_name, test_path=test_path,test_section= test_section, test_result=test_result,
                                 testng_file_name=testng_file_name, test_path_ng=test_path_ng, discrepancy=discrepancy))

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
    test_names_without_path = df[df['test_path'].isin([None, '-'])][Test.TEST_NAME_FIELD].tolist()

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


def write_new_discrepancies_to_csvs(old_csv_path, cur_csv_path, old_test_new_discreps_path, new_tests_new_discreps_path):
    warnings.filterwarnings("ignore", category=UserWarning)

    # Read the CSV files into DataFrames
    old_df = pd.read_csv(old_csv_path)
    cur_df = pd.read_csv(cur_csv_path)

    # Concatenate 'test_name' and 'discrepancy' columns to create a unique identifier
    old_df['unique_identifier'] = old_df[Test.TEST_NAME_FIELD] + "_" + old_df[Test.DISCREPANCY_FIELD]
    cur_df['unique_identifier'] = cur_df[Test.TEST_NAME_FIELD] + "_" + cur_df[Test.DISCREPANCY_FIELD]

    # Identify unique identifiers in the new DataFrame that do not appear in the old DataFrame
    unique_identifiers_old = set(old_df['unique_identifier'])
    unique_identifiers_new = set(cur_df['unique_identifier'])
    identifiers_only_in_new = unique_identifiers_new - unique_identifiers_old

    # Create a new DataFrame with occurrences only in the new DataFrame
    filtered_only_new_df = cur_df[cur_df['unique_identifier'].isin(identifiers_only_in_new)]
    filtered_only_new_df = filtered_only_new_df[filtered_only_new_df[Test.TEST_NAME_FIELD].notnull() & (cur_df[Test.TEST_NAME_FIELD] != '')]
    total_new_discreps = len(filtered_only_new_df)

    # sort to find out which are totally new tests/discrepancies, and which have changed..
    old_test_new_discrep_df = filtered_only_new_df[filtered_only_new_df[Test.TEST_NAME_FIELD].isin(old_df[Test.TEST_NAME_FIELD])]
    num_new_discrep_with_old_tests = len(old_test_new_discrep_df)
    old_test_new_discrep_df.to_csv(old_test_new_discreps_path)

    new_test_new_discrep_df = filtered_only_new_df[~filtered_only_new_df[Test.TEST_NAME_FIELD].isin(old_df[Test.TEST_NAME_FIELD])]
    num_new_discrep_with_new_tests = len(new_test_new_discrep_df)
    new_test_new_discrep_df.to_csv(new_tests_new_discreps_path)

    return [total_new_discreps, num_new_discrep_with_old_tests, num_new_discrep_with_new_tests]



