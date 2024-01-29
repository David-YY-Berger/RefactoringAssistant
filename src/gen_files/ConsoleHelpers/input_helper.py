import os

import src.gen_files
from src.gen_files import gen_scripts as gs, file_utils as fu
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.gen_files.enums import readable
from src.refactor_tests import create_new_files as cnf


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


def get_test_paths_from_input(get_only_test_names = False):

    cmd = get_input_enum_options("How do you want to enter the tests?", list(src.gen_files.enums.OptionsInputTests))
    test_path_list = []
    if cmd == src.gen_files.enums.OptionsInputTests.BY_DIRECTORY_PATH.value:
        src_dir = get_input_ensure_path_valid("Enter the directory that contains the tests (absolute path):", os.path.isdir, "please enter a proper directory path!")
        pf.print_note("Analyzing tests...please wait")
        test_path_list = gs.get_paths_from_dir(src_dir)
        if get_only_test_names:
            return gs.get_names_from_paths(test_path_list)
    else:
        if cmd == src.gen_files.enums.OptionsInputTests.BY_A_LIST_OF_TEST_NAMES.value:
            test_name_list = get_input_list("Enter a list of tests (only one test per line)")
        elif cmd == src.gen_files.enums.OptionsInputTests.BY_PATH_TO_EXCEL_FILE.value:
            test_name_list = get_test_names_from_excel()
        elif cmd == src.gen_files.enums.OptionsInputTests.BY_PATH_TO_CSV_FILE.value:
            test_name_list = get_test_names_from_csv()

        if get_only_test_names:
            return test_name_list

        pf.print_note("Analyzing tests...please wait")
        test_path_list = gs.get_paths_from_test_names(test_name_list)

    test_path_list = cnf.add_base_tests_if_prompted(test_path_list)
    return test_path_list


def get_test_names_from_excel():
    excel_file_path = get_input_ensure_path_valid("Enter the path to the Excel file: ", fu.is_excel_file, "Please enter a path to a valid excel file")
    sheet_list = fu.get_sheets_from_excel(excel_file_path)
    chosen_sheets = get_chosen_items_from_list("Found these sheets in the Excel doc.",
                                                  "Which sheet do you want to read?", sheet_list)
    value_list = []
    for chosen_sheet_name in chosen_sheets:
        vals = fu.read_values_from_sheet_in_excel(excel_file_path=excel_file_path, sheet_name=chosen_sheet_name)
        value_list.extend(vals)
    value_list = [s for s in value_list if isinstance(s, str)]
    return [os.path.basename(item).split('.')[0] for item in value_list]


def get_test_names_from_csv():
    csv_file_path = get_input_ensure_path_valid("Enter the path to the csv file: ", fu.is_csv_file, "Please enter a valid csv file")
    section_list = fu.get_sections_from_csv(csv_file_path)
    section_list = sorted(section_list)
    chosen_sections = get_chosen_items_from_list("Found these sections in the csv doc.",
                                                 "Which section do you want to read?", section_list)
    value_list = []
    for chosen_sheet_name in chosen_sections:
        vals = fu.read_values_from_section_in_csv(csv_file_path=csv_file_path, section_name=chosen_sheet_name)
        value_list.extend(vals)
    value_list = [s for s in value_list if isinstance(s, str)]
    return [os.path.basename(item).split('.')[0] for item in value_list]

