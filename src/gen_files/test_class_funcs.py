import os

from src import application_properties as ap
from src.Classes.test_class import Test
from src.gen_files import constants as cons, paths as p, file_utils as fu
import pandas as pd


def get_names_from_paths(file_paths):
    return [get_name_from_path(path) for path in file_paths]


def get_name_from_path(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def get_main_dir_from_test_path(file_path):
    path_components = os.path.normpath(file_path).split(os.path.sep)
    tests_index = path_components.index('tests') if 'tests' in path_components else -1
    # If 'tests' is found and there is a directory after it, return that directory
    if tests_index != -1 and tests_index + 1 < len(path_components):
        return path_components[tests_index + 1]
    else:
        return cons.empty_char


def build_ng_path(original_path):
    directories, file_name = os.path.split(original_path)
    directories = directories.split(os.path.sep)
    start = directories.index(ap.tests_dir_name) + 1
    root_directory = directories[0] + os.path.sep if directories[0] else ''
    modified_directories = [directory + ap.ng_suffix if index >= start else directory for index, directory in enumerate(directories)]
    modified_directories[0] = root_directory # fix the root directory (it keeps getting messed up..)
    modified_path = os.path.join(*modified_directories, file_name.replace(ap.file_ext, ap.ng_suffix + ap.file_ext))

    return modified_path


def get_test_obj_from_path(file_path):
    return Test(test_name=get_name_from_path(file_path), test_path=file_path, test_section=get_main_dir_from_test_path(file_path))


def get_test_obj_list_from_path_list(file_path_list):
    res = []
    for path in file_path_list:
        res.append(get_test_obj_from_path(path))
    return res


def get_test_obj_from_name(test_name):
    return Test(test_name=test_name)


def get_test_obj_list_w_path_from_name_list(file_names):
    df = pd.read_csv(p.init_dict_file_name_to_path)
    filtered_df = df[df[p.file_name_header].isin(file_names)]

    test_objects = []
    for index, row in filtered_df.iterrows():
        # test_name = row[p.file_name_header]
        test_path = row[p.test_path_header]
        test_obj = get_test_obj_from_path(test_path)
        test_objects.append(test_obj)
    return test_objects


def get_test_obj_list_from_test_name_list(test_name_list):
    res = []
    for test_name in test_name_list:
        res.append(get_test_obj_from_name(test_name))
    return res


def get_paths_from_test_names(lst_test_names):
    # with open(p.temp_dict_test_name_to_path, 'w') as file:
    #     file.write(p.test_name_header + "," + p.test_path_header + "\n")
    # rec_fill_name_to_path_dict(p.all_tests_dir)
    tests_not_found = []
    lst_test_paths = []
    for test_name in lst_test_names:
        test_name = (os.path.splitext(test_name)[0])
        # test_name = test_name.lower();
        test_path = fu.get_val_from_key_csv(csv_path=p.init_dict_file_name_to_path, key_header=p.file_name_header,
                                            val_header=p.test_path_header, key=test_name)
        if test_path == cons.not_found:
            tests_not_found.append(test_name)
        else:
            lst_test_paths.append(test_path)

    if len(tests_not_found) > 0:
        print("\nThese tests were not found in our project (check for typos, ensure spelling matches project code..."
              "Update the Excel sheet, but do not change the code!):")
        for i in tests_not_found:
            print(i)
        print("\n")

    return lst_test_paths


