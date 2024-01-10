import mmap
import os
from src import application_properties as ap
from src.gen_files import file_utils as fu, gen_scripts as gs, constants as cons


def public_sort_tests_to_files(ng_path, non_ng_path, source, cmd):
    test_path_list = []
    if cmd == cons.Cmds.BY_LIST.value:
        test_path_list = gs.get_paths_from_test_names(source)
    if cmd == cons.Cmds.BY_DIR.value:
        test_path_list = gs.get_paths_from_dir(source)
    ng_and_non_ng_tests = sort_ng_tests(test_path_list)
    priv_write_tests_to_output(ng_and_non_ng_tests[0], ng_and_non_ng_tests[1], ng_output_path=ng_path, non_ng_output_path=non_ng_path)


def priv_write_tests_to_output(ng_tests, non_ng_tests, ng_output_path, non_ng_output_path):

    str_ng_tests = ""
    for s in ng_tests:
        str_ng_tests += s + "\n"
    fu.write_to_txt_file(ng_output_path, str_ng_tests)
    print("Wrote " + str(len(ng_tests)) + " tests to " + ng_output_path)

    str_non_ng_tests = ""
    for s in non_ng_tests:
        str_non_ng_tests += s + "\n"
    fu.write_to_txt_file(non_ng_output_path, str_non_ng_tests)
    print("Wrote " + str(len(non_ng_tests)) + " tests to " + non_ng_output_path)

    print("Total test analyzed: " + str(len(ng_tests) + len(non_ng_tests)))


def sort_ng_tests(test_path_lst):
    ng_tests = []
    non_ng_tests = []

    for f_path in test_path_lst:
        with open(f_path, 'rb', 0) as file:  # 'rb' - binary mode. '0' - no buffer
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            is_ng_test = False
            str_to_add = ""
            for word in ap.keywords:
                if s.find(word.encode()) != -1:
                    str_to_add += " | " + word
                    is_ng_test = True
            if is_ng_test == False:
                non_ng_tests.append(f_path)
            else:
                ng_tests.append(os.path.basename(f_path) + str_to_add)

    return [ng_tests, non_ng_tests]

