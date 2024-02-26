import os
import re

import pandas as pd

from src import application_properties as ap
from src.Classes.test_class import Test
from src.gen_files import constants as cons, paths as p, file_utils as fu, gen_scripts as gs
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.test_list_compare.main_test_list_compare import remove_test_obj_duplicates_name_section


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


def get_ng_path_from_orig(original_path):
    directories, file_name = os.path.split(original_path)
    directories = directories.split(os.path.sep)
    start = directories.index(ap.tests_dir_name) + 1
    root_directory = directories[0] + os.path.sep if directories[0] else ''
    modified_directories = [directory + ap.ng_suffix if index >= start else directory for index, directory in enumerate(directories)]
    modified_directories[0] = root_directory # fix the root directory (it keeps getting messed up..)
    modified_path = os.path.join(*modified_directories, file_name.replace(ap.file_ext, ap.ng_suffix + ap.file_ext))

    return modified_path


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
        pf.print_warning("\nCould not find paths for these test names in our project:")
        for i in tests_not_found:
            pf.print_warning(i)
        pf.print_warning("\nPossible reasons why could not find paths:\n"
                         "\t- Typo in the test name entered (search is Case Sensitive!)\n"
                         "\t- Found more than one file with the name entered (program ignores duplicated)\n"
                         "Please double check the test names entered. You can also try by entering a directory.")

    return lst_test_paths


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


def get_path_from_class_name(class_name):
    return p.all_tests_dir + class_name[class_name.find(ap.tests_dir_name) + len(ap.tests_dir_name):].replace('.', os.path.sep) + ap.file_ext


def get_test_obj_from_class_name(class_name):
    return get_test_obj_from_path(get_path_from_class_name(class_name))


def add_path_ng_to_test_obj(test_obj, ignore_warnings = False):
    if test_obj.test_path == cons.empty_char:
        pf.print_warning('No path for test obj ' + test_obj.test_name + '!')
        return

    possible_ng_path = get_ng_path_from_orig(test_obj.test_path)
    if os.path.exists(possible_ng_path):
        test_obj.test_path_ng = possible_ng_path
        return test_obj
    else:
        if not ignore_warnings:
            pf.print_warning("The test: " + test_obj.test_name + " is marked as passed, but could not find it's path at:\n\t" + possible_ng_path)
        test_obj.test_path_ng = cons.empty_char
        return test_obj


def add_path_ng_to_test_obj_list(test_obj_list):
    # tests_no_path_ng = []
    # tests_with_path_ng = []
    # for test in test_obj_list:
    #     result = add_path_ng_to_test_obj(test, ignore_warnings=True)
    #     if result is None:
    #         tests_no_path_ng.append(test)
    #     else:
    #         tests_with_path_ng.append(test)
    #
    # return [tests_with_path_ng, tests_no_path_ng]
    return [add_path_ng_to_test_obj(test, ignore_warnings=True) for test in test_obj_list]


def get_nice_string_list_test_name_section(test_obj_list, include_expected_ng_path = False):
    if len(test_obj_list) == 0:
        return ''
    test_obj_list = remove_test_obj_duplicates_name_section(test_obj_list)
    test_obj_list = Test.order_by_section(test_obj_list)
    dif_max_length = len(max([test.test_name for test in test_obj_list], key=len))
    res = []
    for test in test_obj_list:
        temp = gs.space_nicely(test.test_name, dif_max_length, " | " + test.test_section)
        if include_expected_ng_path:
            temp += '\n\tCurrent path (non ' + ap.ng_suffix + '): \n\t' + test.test_path
            temp += '\n\tExpected path: \n\t' + get_ng_path_from_orig(test.test_path) + '\n\n'
        res.append(temp)
    return res


def get_test_discrep_nice_str(test_obj, max_space):
    res = gs.space_nicely(test_obj.test_name, max_space, " | " + test_obj.test_section + ' | marked as ' + test_obj.test_result + '\n')
    res += extract_function_headers_only(test_obj.discrepancy) + '\n'
    return res


def extract_function_headers_only(content_of_all_functions):
    if content_of_all_functions.__contains__(cons.no_discrepancies_found):
        return "Couldn't locate function, but there might be a discrepancy"

    pattern = r'Function:(.*?)\{'
    matches = re.findall(pattern, content_of_all_functions, re.DOTALL)
    res = ""
    for m in matches:
        res += "Change in Function: " + m.strip() + '\n'
    return res

