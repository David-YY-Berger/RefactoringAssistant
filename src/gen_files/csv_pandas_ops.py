import os.path

import pandas as pd
from src.gen_files import paths as p, gen_scripts as gs, constants as cons
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.Classes.test_class import Test
import warnings

cur_suffix = '_cur'
old_suffix = '_old'


def create_csv_from_test_obj_list(test_obj_list, path):
    df = pd.DataFrame([vars(obj) for obj in test_obj_list])
    df.to_csv(path, index=False)


def create_test_obj_list_from_csv(csv_path, from_cur_suffix = False):
    # Define header names based on the suffix condition
    test_name_header = Test.TEST_NAME_FIELD # never changes
    test_path_header = Test.TEST_PATH_FIELD + cur_suffix if from_cur_suffix else Test.TEST_PATH_FIELD
    test_section_header = Test.TEST_SECTION_FIELD + cur_suffix if from_cur_suffix else Test.TEST_SECTION_FIELD
    test_result_header = Test.TEST_RESULT_FIELD + cur_suffix if from_cur_suffix else Test.TEST_RESULT_FIELD
    testng_file_name_header = Test.TESTNG_FILE_NAME_FIELD + cur_suffix if from_cur_suffix else Test.TESTNG_FILE_NAME_FIELD
    test_path_ng_header = Test.TEST_PATH_NG_FIELD + cur_suffix if from_cur_suffix else Test.TEST_PATH_NG_FIELD
    discrepancy_header = Test.DISCREPANCY_FIELD + cur_suffix if from_cur_suffix else Test.DISCREPANCY_FIELD
    # for non ng content - we take the old suffix!!!
    non_ng_content_header = Test.NON_NG_CONTENT + old_suffix if from_cur_suffix else Test.NON_NG_CONTENT

    df = pd.read_csv(csv_path)
    test_objects = []

    # Iterate over rows in the DataFrame
    for index, row in df.iterrows():
        # Extract values from the row
        test_name = row[test_name_header] if test_name_header in df.columns else 'Error didnt find test name column in csv!'
        test_path = row[test_path_header] if test_path_header in df.columns else cons.empty_char
        test_section = row[test_section_header] if test_section_header in df.columns else cons.empty_char
        test_result = row[test_result_header] if test_result_header in df.columns else cons.empty_char
        testng_file_name = row[testng_file_name_header] if testng_file_name_header in df.columns else cons.empty_char
        test_path_ng = row[test_path_ng_header] if test_path_ng_header in df.columns else cons.empty_char
        discrepancy = row[discrepancy_header] if discrepancy_header in df.columns else cons.empty_char
        non_ng_content = row[non_ng_content_header] if non_ng_content_header in df.columns else cons.empty_char

        # Create a Test object and append it to the list
        test_objects.append(Test(test_name, test_path=test_path,test_section= test_section, test_result=test_result,
                                 testng_file_name=testng_file_name, test_path_ng=test_path_ng, discrepancy=discrepancy,
                                 non_ng_content=non_ng_content))

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

    old_df = pd.read_csv(old_csv_path)
    cur_df = pd.read_csv(cur_csv_path)

    old_tests_df = cur_df[cur_df[Test.TEST_NAME_FIELD].isin(old_df[Test.TEST_NAME_FIELD])]
    new_tests_w_new_discrep_df = cur_df[~cur_df[Test.TEST_NAME_FIELD].isin(old_df[Test.TEST_NAME_FIELD])]

    # Find discrepancies in old tests that are different from old_df
    merged_df = pd.merge(old_tests_df, old_df, on=Test.TEST_NAME_FIELD, suffixes=(cur_suffix, old_suffix))
    old_tests_new_discrep_df = merged_df[merged_df[Test.DISCREPANCY_FIELD + cur_suffix] != merged_df[Test.DISCREPANCY_FIELD + old_suffix]]

    # Write to CSV files
    old_tests_new_discrep_df.to_csv(old_test_new_discreps_path, index=False)
    new_tests_w_new_discrep_df.to_csv(new_tests_new_discreps_path, index=False)
    num_new_discrep_with_old_tests = len(old_tests_new_discrep_df)
    num_new_discrep_with_new_tests = len(new_tests_w_new_discrep_df)
    total_new_discreps = num_new_discrep_with_old_tests + num_new_discrep_with_new_tests

    return [total_new_discreps, num_new_discrep_with_old_tests, num_new_discrep_with_new_tests]




