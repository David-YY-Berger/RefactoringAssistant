import os

import src.gen_files
from src.gen_files import gen_scripts as gs, paths as p
from src.gen_files.ConsoleHelpers import print_functions as pf
from src.refactor_tests import create_new_files as cnf, sort_tests_to_files as sort_tests


def readable(str):
    return str.capitalize().replace('_', ' ')


def get_input_enum_options(prompt, option_list):
    print(prompt + " (Enter just the number)")
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
    while (buf != "end"):
        input_list.append(buf)
        buf = input()
    input_list = [s for s in input_list if not s.isspace()]
    return input_list


def get_input_ensure_valid(prompt, boolean_function, error_msg):
    buf = ''
    while True:
        buf = input(prompt)
        if boolean_function(buf):
            return buf
        else:
            print(error_msg)


def get_chosen_items_from_list(init_prompt, enter_list_prompt, option_list):
    pf.print_note('\n' + init_prompt)
    print(enter_list_prompt +
          "\nSeparate numbers by whitespace. Enter 'end' to finish: ")
    select_all = 'Select all - recommended'
    option_list = [select_all] + option_list

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
    if(res.__contains__(select_all)):
        option_list.remove(select_all)
        return option_list
    else:
        return res


def get_tests_from_input():

    cmd = get_input_enum_options("How do you want to enter the tests?", list(src.gen_files.enums.OptionsInputTests))
    test_path_list = []
    if cmd == src.gen_files.enums.OptionsInputTests.BY_DIRECTORY_PATH.value:
        src_dir = get_input_ensure_valid("Enter the directory that contains the tests (absolute path):", os.path.isdir, "please enter a proper directory path!")
        pf.print_note("Analyzing tests...please wait")
        test_path_list = gs.get_paths_from_dir(src_dir)
    elif cmd == src.gen_files.enums.OptionsInputTests.BY_A_LIST_OF_TEST_NAMES.value:
        test_name_list = get_input_list("Enter a list of tests (only one test per line)")
        pf.print_note("Analyzing tests...please wait")
        test_path_list = gs.get_paths_from_test_names(test_name_list)
    elif cmd == src.gen_files.enums.OptionsInputTests.BY_PATH_TO_EXCEL_FILE.value:
        print("coming soon!")
        exit(0)
    test_path_list = cnf.add_base_tests_if_prompted(test_path_list)

    return test_path_list
