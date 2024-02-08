import difflib
import os.path
import sys
import re


import src.gen_files.test_class_funcs
from src.gen_files import (constants as cons, paths as p, gen_scripts as gs, file_utils as fu, test_class_funcs as tcf,
                           csv_pandas_ops as cpo, enums as enums, stats_for_metrics as sfm)
from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf
from src import application_properties as ap
from src.refactor_tests import create_new_test_files as cntf

this_discrepancy_csv_path = os.path.join(p.output_dir, 'discrepancies_' + gs.get_date() + '.csv')
tests_passed_missing_ng_path_text_path = os.path.join(p.output_dir, 'tests_marked_as_passed_but_missing_ng_path.txt')
tests_to_mark_no_code_change_text_path = os.path.join(p.output_dir, 'tests_marked_as_passed_but_could_be_marked_as_no_code_change.txt')


def main_script():

    pf.print_step_separator("Discrepancy  Tracker")
    cmd = ih.get_input_enum_options('What would you like to do?', list(enums.DiscrepancyTrackerOptions))
    if cmd == enums.DiscrepancyTrackerOptions.FIND_DISCREPANCIES.value:

        pf.print_step_separator("Step 1: Enter and Analyze Tests")
        test_objs = ih.get_test_objs_from_excel()
        pf.print_note("Searching for file paths for each test...")
        passed_tests_with_paths = get_passed_tests_with_paths(test_objs)

        print("\n")
        pf.print_step_separator("Step 2: Discrepancies and Other Results")
        pf.print_note("Ensuring that all tests have an ng file path with proper suffix (" + ap.ng_suffix + ")...")
        [num_tests_with_no_path_ng, passed_tests_with_path_and_ng_paths] = remove_tests_with_no_ng_path(passed_tests_with_paths)
        pf.print_warning("Found "+ str(num_tests_with_no_path_ng) + " tests marked as 'passed' or 'passed without code change', "
                "but could not find the path to the new ng file!\nPlease that that tests' ng paths are written as expected.\n"
                         "Wrote these tests to: " + tests_passed_missing_ng_path_text_path)

        pf.print_note("Scanning for Discrepancies...")
        [num_files_with_discrepancies, num_files_no_discrepancies] = find_and_write_discrepancies(passed_tests_with_path_and_ng_paths)
        pf.print_note("Totals tests analyzed (with correct ng path): " + str(num_files_with_discrepancies + num_files_no_discrepancies)
                      + "\nTests with descrepancies: " + str(num_files_with_discrepancies)
                      + "\nTests with no descrepances: " + str(num_files_no_discrepancies)
                      + "\n")
        pf.print_note("Wrote discrepancies to: " + this_discrepancy_csv_path)

        files_created = overwrite_files_if_prompted()

        sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(),
                            time=gs.get_time(),product=sfm.product_names.Discrepancy_Tracker.name, is_success=True,
                             tests_analyzed=(num_files_no_discrepancies+num_files_with_discrepancies),
                            total_files_with_descrepancies=num_files_with_discrepancies, total_files_without_descrepancies=num_files_no_discrepancies,
                            passed_tests_with_no_ng_path=tests_passed_missing_ng_path_text_path,
                            ng_files_overwritten=files_created)


    elif cmd == enums.DiscrepancyTrackerOptions.COMPARE_DISCREPANCIES.value:
        compare_discrepancies()
        # sfm.append_to_stats()
    else:
        print('error!')
        return
    # find_and_write_discrepancies()


def get_passed_tests_with_paths(test_objs):
    test_objs = get_test_objs_with_path(test_objs)
    tests_passed_with_or_without_code_change = [test for test in test_objs if test.test_result == ap.excel_result_passed
                                                or test.test_result == ap.excel_result_passed_wo_code_change]
    return tcf.add_path_ng_to_test_obj_list(tests_passed_with_or_without_code_change)


def remove_tests_with_no_ng_path(test_obj_list):
    # separate tests without proper ng path, print to output
    tests_with_no_path_ng = [test for test in test_obj_list
                             if test.test_path_ng == cons.empty_char]
    num_tests_no_path_ng = len(tests_with_no_path_ng)
    str_of_all_tests_no_path_ng = tcf.get_nice_string_list_test_name_section(tests_with_no_path_ng,
                                                                             include_expected_ng_path=True)
    fu.write_txt_to_file(tests_passed_missing_ng_path_text_path, gs.open_list_as_string(str_of_all_tests_no_path_ng, ''))

    tests_with_path_ng = [test for test in test_obj_list if test.test_path_ng != cons.empty_char]
    return [num_tests_no_path_ng, tests_with_path_ng]


def find_and_write_discrepancies(test_obj_list):

    num_files_with_discrepancies = 0
    num_files_no_discrepancies = 0
    tests_marked_passed_but_really_no_code_change = []


    test_objs_with_discrepancies = []
    for test in (test_obj_list):
        discrepancies = compare_files_by_function(test.test_path, test.test_path_ng)
        if discrepancies:
            num_files_with_discrepancies += 1
            # pf.print_header(test.test_name)
            res = test.test_name + ":\n"
            res += get_discrepancies_str_by_function(discrepancies, os.path.splitext(os.path.basename(test.test_path))[0],
                                              os.path.splitext(os.path.basename(test.test_path_ng))[0])
            res += '\n'
            test.discrepancy = res
            test_objs_with_discrepancies.append(test)
        else:
            if test.test_result == ap.excel_result_passed: # but didn't find discrepancy
                tests_marked_passed_but_really_no_code_change.append(test)
            num_files_no_discrepancies += 1
            # print('no discrepancy: ' + test.test_name)

    cpo.create_csv_from_test_obj_list(test_objs_with_discrepancies, this_discrepancy_csv_path)

    str_of_test_to_mark_no_code_change = tcf.get_nice_string_list_test_name_section(tests_marked_passed_but_really_no_code_change)
    fu.write_txt_to_file(tests_to_mark_no_code_change_text_path,
                         gs.open_list_as_string(str_of_test_to_mark_no_code_change, '\n'))

    print(' ')
    pf.print_note('Found ' + str(len(tests_marked_passed_but_really_no_code_change)) + ' tests marked as "passed", '
            'but found no discrepency between regular and ng files...\n' +
                  'Recommended to mark these tests as "passed without code change" to allow overwrite.')
    pf.print_note("Wrote these tests (by section) to: " + tests_to_mark_no_code_change_text_path)
    print(' ')

    return [num_files_with_discrepancies, num_files_no_discrepancies]


def get_test_objs_with_path(test_objs):

    temp_csv_path = os.path.join(p.temp_dir, 'temp_copy.csv')
    cpo.create_csv_from_test_obj_list(test_objs, p.temp_csv_of_test_obj)
    cpo.write_paths_to_test_objs(p.temp_csv_of_test_obj, p.init_dict_file_name_to_path, temp_csv_path,
                                 ignore_warning=True)
    cpo.remove_tests_with_no_path(temp_csv_path, temp_csv_path)
    test_objs_with_path = cpo.create_test_obj_list_from_csv(temp_csv_path)
    # list_tests_passed = [test for test in test_objs_with_path if test.test_result == ap.excel_result_passed]
    # list_tests_passed_no_code_change = [test for test in test_objs_with_path if
    #                                     test.test_result == ap.excel_result_passed_wo_code_change]
    # return [list_tests_passed, list_tests_passed_no_code_change]
    return test_objs_with_path

def compare_discrepancies():
    f = ''


def get_java_functions(file_content):
    # Regular expression to match Java functions
    pattern = re.compile(r'\b(?:public|private|protected|static|\s)+\w+\s+\w+\([^)]*\)\s*{')
    matches = pattern.finditer(file_content)
    functions = []
    for match in matches:
        functions.append(match.group())
    return functions


def compare_files_by_function(file1, file2):


    content1 = fu.read_file_content_as_str(file1)
    content2 = fu.read_file_content_as_str(file2)
    functions1 = get_java_functions(content1)
    functions2 = get_java_functions(content2)

    file_name1 = os.path.splitext(os.path.basename(file1))[0]
    file_name2 = os.path.splitext(os.path.basename(file2))[0]

    discrepancies_by_function = {}

    for function in set(functions1 + functions2):
        num_close_brackets = get_num_closing_brackets(function, content1)

        pattern = re.escape(function) + r'[^}]*?\}' * num_close_brackets

        lines1 = re.search(pattern, content1, re.DOTALL)
        lines2 = re.search(pattern, content2, re.DOTALL)

        if lines1 and lines2:
            lines1 = lines1.group().strip()
            lines2 = lines2.group().strip()

            if lines1 != lines2:
                discrepancies_by_function[function] = {
                    file_name1: lines1,
                    file_name2: lines2
                }

    return discrepancies_by_function


def get_discrepancies_str_by_function(discrepancies_by_function, file1_name, file2_name):
    if not discrepancies_by_function:
        return "No discrepancies found."
    else:
        res = ''
        for function, discrepancy in discrepancies_by_function.items():
            res += f"Function: {function}"
            res += get_string_diff(str(discrepancy[file1_name]), str(discrepancy[file2_name]) + "\n")
        return res

def get_num_closing_brackets(function_header, content):
    """
    :param function_header: looks like: 'private void initParams() {'
    :return: gets the number of closing brackets expecting after this function header
    """
    res = 1 # function header includes a '{'
    stack = ['{']
    content = content[content.find(function_header) + len(function_header):]

    # last_brace_index = None
    for i, char in enumerate(content):
        if len(stack) == 0:
            break
        if char == '{':
            stack.append(i)
            res += 1
        elif char == '}':
            if stack:
                # last_brace_index = (
                stack.pop()
            else:
                # If there are extra closing braces
                raise ValueError("Extra '}' found without a corresponding '{'")

    return res


def get_string_diff(str1, str2):
    d = difflib.Differ()
    diff = list(d.compare(str1.splitlines(), str2.splitlines()))
    res = ""
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            res += line + "\n"
    return res


def overwrite_files_if_prompted():
    cmd = ih.get_input_enum_options(
        "For the tests marked as 'passed without code change', would you like to overwrite the 'ng' files with "
        "the content of the non ng files?",
        list(src.gen_files.enums.OptionsYesNo),
        "Warning - cannot be undone..")
    if cmd == src.gen_files.enums.OptionsYesNo.YES.value:
        entered_password = input('enter password:')
        if entered_password != 'admin_password_overwrite':
            print('wrong password!')
            return
        else:
            test_obj_w_discrepancies = cpo.create_test_obj_list_from_csv(this_discrepancy_csv_path)
            test_obj_w_discrepancies_passed_no_code_change = [test for test in test_obj_w_discrepancies if test.test_result == ap.excel_result_passed_wo_code_change]
            for test in test_obj_w_discrepancies_passed_no_code_change:
                cntf.create_ng_file(test.test_path, overwrite=True)


if __name__ == '__main__':
    main_script()

