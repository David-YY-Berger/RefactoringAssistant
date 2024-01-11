import mmap
import os
import shutil

import sort_tests_to_files as sort_tests
import create_playlist_from_files as cp
from src.gen_files import constants as cons, input_helper as ih, paths as p


def main_script():
    init_params()

    get_input_and_sort_tests_to_files()
    # create_NG_versions_of_all_tests()
    cp.public_create_playlist_from_files(p.output_dir, non_ng_tests_path=p.non_ng_tests_dir_path)


def get_input_and_sort_tests_to_files():

    cmd = ih.get_input_options("How do you want to enter the tests?", list(cons.OptionsInputTests))
    if cmd == cons.OptionsInputTests.BY_DIRECTORY_PATH.value:
        src_dir = ih.get_input_ensure_valid("Enter the directory that contains the tests (absolute path):", os.path.isdir, "please enter a proper directory path!")
        sort_tests.public_sort_tests_to_files(source=src_dir, ng_path=p.ng_tests_dir_path, non_ng_path=p.non_ng_tests_dir_path, cmd=cmd)
    elif cmd == cons.OptionsInputTests.BY_A_LIST_OF_TEST_NAMES.value:
        test_name_list = ih.get_input_list("Enter a list of tests")
        sort_tests.public_sort_tests_to_files(source=test_name_list, ng_path=p.ng_tests_dir_path, non_ng_path=p.non_ng_tests_dir_path, cmd=cmd)


def init_params():
    global cur_dir, ng_path, non_ng_path
    shutil.rmtree(p.output_dir)
    os.makedirs(p.output_dir)


if __name__ == '__main__':
    main_script()
