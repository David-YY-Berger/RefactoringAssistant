import mmap
import os
import shutil

import sort_tests_to_files as sort_tests
import create_playlist_from_files as cp
from src.gen_files import constants as cons


src_dir = ng_path = non_ng_path = ""
cur_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cur_dir, "..", "..", "output")


def main_script():
    init_params()

    get_input_and_sort_tests_to_files()
    # create_NG_versions_of_all_tests()
    cp.public_create_playlist_from_files(output_dir, non_ng_tests_path=non_ng_path)


def get_input_and_sort_tests_to_files():
    not_finished = True
    cmd = ""
    while (not_finished):
        not_finished = False
        cmd = int(input("Enter tests by:\n" +
                        str(cons.Cmds.BY_DIR.value) + ". " + cons.Cmds.BY_DIR.name + "\n" +
                        str(cons.Cmds.BY_LIST.value) + ". " + cons.Cmds.BY_LIST.name + "\n"))
        if cmd >= len(cons.Cmds):
            print("Pls Re-Enter")
            not_finished = True
    if cmd == cons.Cmds.BY_DIR.value:
        src_dir = input("Enter the directory holds the tests (absolute path):")
        sort_tests.public_sort_tests_to_files(source=src_dir, ng_path=ng_path, non_ng_path=non_ng_path, cmd=cmd)
    elif cmd == cons.Cmds.BY_LIST.value:
        test_name_list = get_test_names_from_input()
        sort_tests.public_sort_tests_to_files(source=test_name_list, ng_path=ng_path, non_ng_path=non_ng_path, cmd=cmd)


def init_params():
    global src_dir, cur_dir, ng_path, non_ng_path
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    ng_path = os.path.join(output_dir,  "tests_containing_ng.txt")
    non_ng_path = os.path.join(output_dir, "tests_do_not_contain_ng.txt")


def get_test_names_from_input():
    print("Enter list of tests. Type 'end' when finished")
    test_name_list = []
    buf = " "
    while (buf != "end"):
        test_name_list.append(buf)
        buf = input()
    test_name_list = [s for s in test_name_list if not s.isspace()]
    return test_name_list


if __name__ == '__main__':
    main_script()
