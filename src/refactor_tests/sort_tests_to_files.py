import mmap
import os
from src import application_properties as ap
from src.gen_files import file_utils as fu, gen_scripts as gs, constants as cons
from src.gen_files.ConsoleHelpers import print_functions as pf


def public_sort_tests_to_files(ng_path, non_ng_path, test_path_list):
    ng_and_non_ng_tests = sort_ng_tests(test_path_list)
    priv_write_tests_to_output(ng_and_non_ng_tests[0], ng_and_non_ng_tests[1], ng_output_path=ng_path,
                               non_ng_output_path=non_ng_path)


def priv_write_tests_to_output(ng_tests, non_ng_tests, ng_output_path, non_ng_output_path):
    num_ng_tests = len(ng_tests)
    num_non_ng_tests = len(non_ng_tests)
    str_ng_tests = ("Tests that contain 'ng' phrases: \n"
                    "(For every test, search for the phrase, find a solution, and run the test)\n\n")
    for s in ng_tests:
        str_ng_tests += s + "\n"
        str_ng_tests += cons.line + "\n"
    fu.write_txt_to_file(ng_output_path, str_ng_tests)

    pf.print_note("Found " + str(num_ng_tests) + " tests that contain ng substrings, and " + str(num_non_ng_tests) + " tests that do not contain ng substrings")

    pf.print_note("Wrote tests containing ng substrings to " + ng_output_path + "\n")

    str_non_ng_tests = ""
    for s in non_ng_tests:
        str_non_ng_tests += s + "\n"
    fu.write_txt_to_file(non_ng_output_path, str_non_ng_tests)

    pf.print_note("Wrote tests that do not contain ng substrings to " + non_ng_output_path)
    percentage = (num_ng_tests / (num_ng_tests + num_non_ng_tests)) * 100
    pf.print_note("Analyzed " + str(num_ng_tests + num_non_ng_tests) + f" tests. Found that {percentage:.2f}% contain ng substrings")


def sort_ng_tests(test_path_lst):
    ng_tests = []
    non_ng_tests = []
    max_length_test_name = max(map(len, [os.path.splitext(os.path.basename(s))[0] for s in test_path_lst]))

    for f_path in test_path_lst:
        with open(f_path, 'rb', 0) as file:  # 'rb' - binary mode. '0' - no buffer
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            is_ng_test = False
            str_to_add_ng_tests = "contains:"
            test_name = os.path.splitext(os.path.basename(f_path))[0]
            for word in ap.keywords:
                if s.find(word.encode()) != -1:  # if test contains ng functions
                    str_to_add_ng_tests += " | " + word
                    is_ng_test = True
            # place test in appropriate list
            if not is_ng_test:
                non_ng_tests.append(f_path)
            else:
                ng_tests.append(gs.space_nicely(test_name, max_length_test_name, str_to_add_ng_tests))

    return [ng_tests, non_ng_tests]
