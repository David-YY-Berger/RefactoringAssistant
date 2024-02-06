import pandas as pd
from src.gen_files import paths as p, gen_scripts as gs, constants as cons
from src.gen_files.ConsoleHelpers import print_functions as pf


def create_csv_from_test_obj_list(test_obj_list, path):
    df = pd.DataFrame([vars(obj) for obj in test_obj_list])
    df.to_csv(path, index=False)


def write_paths_to_test_objs(test_obj_csv_path, test_to_path_csv_path, output_path =''):
    # Read the CSV files

    test_to_paths = pd.read_csv(test_to_path_csv_path)
    duplic_in_test_to_path = find_non_unique_values(test_to_path_csv_path, p.test_name_header)
    if len(duplic_in_test_to_path) > 0:
        pf.print_warning("Found duplicates test names in project (" + test_to_path_csv_path + '):\n' +
                         gs.open_list_as_string(duplic_in_test_to_path, '\n')
                         + '\n ignoring the duplicates..')
        test_to_paths = test_to_paths.drop_duplicates(subset='test_name', keep=False)

    test_objs = pd.read_csv(test_obj_csv_path)
    duplic_in_test_obj = find_non_unique_values(test_obj_csv_path, p.test_name_header)
    if len(duplic_in_test_obj) > 0:
        pf.print_warning("Found duplicates in " + test_obj_csv_path + ':\n' +
                         gs.open_list_as_string(duplic_in_test_obj, '\n')
                         + '\n ignoring the duplicates..')
        test_objs = test_objs.drop_duplicates(subset='test_names', keep=False)


    # think, and write creafully to chatgpt

    # # Merge the DataFrames on 'test_name'
    # merged_df = pd.merge(test_objs, test_to_paths, on='test_name', how='inner') #remove whatever tests don't appear in both
    # # Identify test_names with no path
    # test_names_with_no_path = test_objs.loc[~test_objs['test_name'].isin(merged_df['test_name']), 'test_name'].tolist()
    #
    # # Print test_names_with_no_path
    # pf.print_warning("Did not find paths for these test names (ignoring these tests):")
    # pf.print_warning(gs.open_list_as_string(test_names_with_no_path, '\n'))





    # Overwrite the current test_obj_list CSV with the new joined CSV
    if not output_path:
        output_path = test_obj_csv_path
    merged_df.to_csv(output_path, index=False)


def find_non_unique_values(csv_path, col_header):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_path)

    # Find and return values that are not unique in the specified column
    non_unique_values = df[df.duplicated(col_header, keep=False)][col_header].tolist()
    return list(set(non_unique_values))


