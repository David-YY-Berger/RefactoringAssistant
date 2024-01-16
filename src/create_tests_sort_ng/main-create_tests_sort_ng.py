import mmap
import os
import shutil

import sort_tests_to_files as sort_tests
import create_playlist_from_files as cp
import create_new_files as cnf
import src.application_properties as ap
import src.gen_files.enums
from src.gen_files import constants as cons, input_helper as ih, paths as p, gen_scripts as gs


def main_script():
    init_params()

    test_path_list = get_input_and_sort_tests_to_files()
    print(cons.END_OF_SECTION)
    create_ng_tests_if_prompted(test_path_list=test_path_list)
    print(cons.END_OF_SECTION)
    # cp.public_create_playlist_from_files(p.output_dir, non_ng_tests_path=p.non_ng_tests_dir_path)
    # print(cons.END_OF_SECTION)


def get_input_and_sort_tests_to_files():

    cmd = ih.get_input_enum_options("How do you want to enter the tests?", list(src.gen_files.enums.OptionsInputTests))
    test_path_list = []
    if cmd == src.gen_files.enums.OptionsInputTests.BY_DIRECTORY_PATH.value:
        src_dir = ih.get_input_ensure_valid("Enter the directory that contains the tests (absolute path):", os.path.isdir, "please enter a proper directory path!")
        test_path_list = gs.get_paths_from_dir(src_dir)
    elif cmd == src.gen_files.enums.OptionsInputTests.BY_A_LIST_OF_TEST_NAMES.value:
        test_name_list = ih.get_input_list("Enter a list of tests (only one test per line)")
        test_path_list = gs.get_paths_from_test_names(test_name_list)
    elif cmd == src.gen_files.enums.OptionsInputTests.BY_PATH_TO_EXCEL_FILE.value:
        print("coming soon!")
        exit(0)
    test_path_list = cnf.add_base_tests_if_prompted(test_path_list)
    sort_tests.public_sort_tests_to_files(ng_path=p.ng_tests_dir_path, non_ng_path=p.non_ng_tests_dir_path,
                                          test_path_list=test_path_list)
    return test_path_list


def create_ng_tests_if_prompted(test_path_list):
    cmd = ih.get_input_enum_options("Would you like to create ng directories and files (with a " + ap.ng_suffix + " suffix)?\n"
                                    + "If the " + ap.ng_suffix + " test already exists, the program will not overwrite it.\n"
                                    + "Warning - cannot undo creating the files programmatically\n",
                                    list(src.gen_files.enums.OptionsYesNo))
    if cmd == src.gen_files.enums.OptionsYesNo.YES.value:
        cnf.create_ng_versions_of_all_tests(test_path_list)
    # elif cmd == cons.OptionsYesNo.NO.value:


def init_params():
    global cur_dir, ng_path, non_ng_path
    shutil.rmtree(p.output_dir)
    os.makedirs(p.output_dir)


if __name__ == '__main__':
    main_script()
