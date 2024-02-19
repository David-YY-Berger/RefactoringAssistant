import os
import sys

import src.Classes.test_class
import src.gen_files
import src.gen_files.test_class_funcs
import src.refactor_tests.create_new_test_files
from src.gen_files import (gen_scripts as gs, file_utils as fu, test_class_funcs as tcf, constants as cons,
                           csv_pandas_ops as cpo, paths as p)
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.gen_files.enums import readable
from src import application_properties as ap
from src.Classes import test_class


def get_input_enum_options(prompt, option_list, warning = None):
    print(prompt)
    if warning:
        pf.print_warning(warning)
    print(" (Enter just the number)")
    possible_options = []
    for op in option_list:
        print(str(op.value) + ". " + readable(op.name))
        possible_options.append(str(op.value))
    keep_going = True
    while keep_going:
        cmd = input()
        if not cmd.isnumeric():
            print("Please enter a number")
        elif cmd not in possible_options:
            print("Please only enter one of the given options")
        else:
            keep_going = False
            return int(cmd)


def get_input_list(prompt):
    print(prompt + ". Enter 'end' to finish")
    input_list = []
    buf = " "
    while buf.lower() != "end":
        input_list.append(buf)
        buf = input()
    input_list = [s for s in input_list if not s.isspace()]
    return input_list


def get_input_ensure_path_valid(prompt, boolean_function, error_msg):
    buf = ''
    while True:
        buf = input(prompt).replace('"',''). replace("'", "")
        if boolean_function(buf):
            return buf
        else:
            print(error_msg)


def get_chosen_items_from_list(init_prompt, enter_list_prompt, option_list):
    """

    :param init_prompt:
    :param enter_list_prompt:
    :param option_list:
    :return: list of chosen options as strings
    """
    pf.print_note('\n' + init_prompt)
    print(enter_list_prompt +
          "\nSeparate numbers by whitespace. Enter 'end' to finish: ")
    select_all = 'Select all'
    none = 'None'
    option_list = [select_all, none] + option_list

    for i, option in enumerate(option_list, start=1):
        print(f"{i}. {option}")
    res = set()

    while True:
        user_input = input()
        if user_input.lower() == 'end':
            break
        try:
            # Split the input into a list of integers
            choices = {int(choice) for choice in user_input.split()}
            res.update(option_list[choice - 1] for choice in choices if 1 <= choice <= len(option_list))
        except ValueError:
            print("Invalid input. Please enter valid numbers separated by whitespace.")
    if res.__contains__(select_all):
        option_list.remove(select_all)
        option_list.remove(none)
        return option_list
    if len(res) == 1 and res.__contains__(none):
        return []
    else:
        if res.__contains__(none):
            res.remove(none)
        return res


def get_test_objs_from_input(get_test_paths_always = False, get_source_type=False):
    """
    :param get_source_type:
    :param get_test_paths_always: look for tests in projects, get test path. if can't find, them remove these test objects without paths
    :return: List of Test obj (with all fields, unless specified)
    """
    cmd = get_input_enum_options("How do you want to enter the tests?", list(src.gen_files.enums.OptionsInputTests))
    src_type = cons.empty_char
    test_obj_list = []
    if cmd == src.gen_files.enums.OptionsInputTests.BY_DIRECTORY_PATH.value:
        src_dir = get_input_ensure_path_valid("Enter the directory that contains the tests (absolute path):", os.path.isdir, "please enter a proper directory path!")
        pf.print_note("Analyzing tests...please wait")
        path_list_without_basenames = gs.get_paths_from_dir(src_dir)
        test_obj_list = src.gen_files.test_class_funcs.get_test_obj_list_from_path_list(path_list_without_basenames)
        src_type = src_dir
    else:
        if cmd == src.gen_files.enums.OptionsInputTests.BY_A_LIST_OF_TEST_NAMES.value:
            test_obj_list = src.gen_files.test_class_funcs.get_test_obj_list_from_test_name_list(get_input_list("Enter a list of tests (only one test per line)"))
            src_type = 'list of tests'
        elif cmd == src.gen_files.enums.OptionsInputTests.BY_PATH_TO_EXCEL_FILE.value:
            test_obj_list = get_test_objs_from_excel()
            src_type = 'excel'
        elif cmd == src.gen_files.enums.OptionsInputTests.BY_PATH_TO_CSV_FILE.value:
            test_obj_list = get_test_objs_from_csv()
            src_type = 'csv'
        elif cmd == src.gen_files.enums.OptionsInputTests.GET_ALL_TESTS_IN_TESTNG_FILES.value:
            pf.print_note("Analyzing tests...please wait")
            test_names = gs.get_all_test_names_in_testng_files()
            test_obj_list = src.gen_files.test_class_funcs.get_test_obj_list_w_path_from_name_list(test_names)
            # @todo
            # get the testng as a field in testobj here... merge df maps w pandas
            src_type = 'all tests found in testng files'
        else:
            print('failed to receive cmd!')
            return

        if get_test_paths_always:
            test_names_list = [test.test_name for test in test_obj_list]
            paths = tcf.get_paths_from_test_names(test_names_list)
            test_obj_list = src.gen_files.test_class_funcs.get_test_obj_list_from_path_list(paths)

    if get_source_type:
        return [test_obj_list, src_type]
    else:
        return test_obj_list


def get_test_objs_from_excel():
    excel_file_path = get_input_ensure_path_valid("Enter the path to the Excel file: ", fu.is_excel_file, "Please enter a path to a valid excel file")
    sheet_list = fu.get_sheets_from_excel(excel_file_path)
    chosen_sheets = get_chosen_items_from_list("Found these sheets in the Excel doc.",
                                                  "Which sheet do you want to read?", sheet_list)
    test_obj_list = []
    seen_test_names = set()
    pf.print_note("Analyzing tests...please wait")
    for chosen_sheet_name in chosen_sheets:
        test_and_results_lst = fu.read_test_names_and_results_from_sheet_in_excel(excel_file_path=excel_file_path, sheet_name=chosen_sheet_name)
        if not test_and_results_lst:
            test_and_results_lst = [' ']
        test_and_results_lst = [s for s in test_and_results_lst if isinstance(s, test_class.TestAndResult) and isinstance(s.test_name, str)]
        for item in test_and_results_lst:
            item.test_name = gs.trim_suffix(item.test_name)
            # Check if the test_name is not in the set of seen test_names
            if item.test_name not in seen_test_names:
                test_obj_list.append(
                    test_class.Test(test_name=item.test_name, test_result=item.test_result,
                                    test_section=chosen_sheet_name))
                seen_test_names.add(item.test_name)
    return test_obj_list


def get_test_objs_from_csv():
    csv_file_path = get_input_ensure_path_valid("Enter the path to the csv file: ", fu.is_testrail_csv,
                                                "Please ensure that path leads to a valid csv file, "
                                                "with column headers: " + gs.open_list_as_string(ap.csv_all_column_headers, ","))
    section_list = fu.get_sections_from_csv(csv_file_path)
    section_list = sorted(section_list)
    chosen_sections = get_chosen_items_from_list("Found these sections in the csv doc.",
                                                 "Which section do you want to read?", section_list)
    test_obj_list = []
    pf.print_note("Analyzing tests...please wait")
    for chosen_section in chosen_sections:
        vals = fu.read_values_from_section_in_csv(csv_file_path=csv_file_path, section_name=chosen_section)
        if not vals:
            vals = [' ']
        vals = [s for s in vals if isinstance(s, str)]
        vals = [os.path.basename(item).split('.')[0] for item in vals]  # remove the '.test1'
        for val in vals:
            test_obj_list.append(test_class.Test(test_name=val, test_section='Section: ' + chosen_section))
    return test_obj_list


def reassign_project_path():
    pf.print_warning('Could not find path to test folder')
    new_path = input("[It should something like this: " + r'C:\urm\workspace-1.0.0.2-URM\alma_itest_ux\src\test ]' + '\n'
                        "Please add the path (of the test folder) to this file: " + p.test_project_base_txt_file_path + '\n' +
                     'Or, enter the path here:\n')
    fu.write_txt_to_file(p.test_project_base_txt_file_path, new_path)
    pf.print_note("Exit the program and restart")
    input('Press any key to continue')
    sys.exit()