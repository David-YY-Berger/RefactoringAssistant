import os.path
import re

import src.gen_files.test_class_funcs
from src.gen_files import (constants as cons, paths as p, gen_scripts as gs, file_utils as fu, test_class_funcs as tcf,
                           csv_pandas_ops as cpo, enums as enums, stats_for_metrics as sfm)
from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf
from src import application_properties as ap
from src.gen_files.gen_scripts import get_string_diff
from src.refactor_tests import create_new_test_files as cntf

# csv/data files:
cur_discrepancy_csv_path = os.path.join(p.discrep_tracker_output_dir, 'cur_discrepancies_' + gs.get_date() + '.csv')
only_new_discrepancy_csv_path = os.path.join(p.discrep_tracker_output_dir, 'temp_only_new_discrepancies_.csv')
new_tests_new_discreps_csv_path = os.path.join(p.discrep_tracker_output_dir, 'temp_new_tests_new_discreps_.csv')
old_tests_new_discreps_csv_path = os.path.join(p.discrep_tracker_output_dir, 'temp_old_tests_new_discreps_.csv')
changes_in_non_ng_files_csv_path = os.path.join(p.discrep_tracker_output_dir, 'temp_changes_in_non_ng_files.csv')

# output/report files:
discrep_by_section_output_dir = os.path.join(p.discrep_tracker_output_dir, 'discrepancies_by_section')
tests_passed_missing_ng_path_text_path = os.path.join(p.discrep_tracker_output_dir,
                                                      'tests_marked_as_passed_but_missing_ng_path.txt')

max_char_count_allowed_by_pandas = 30000


def main_script():
    """
    imperfections:
    - files longer than 30,000 chars get cut off
    - reorganized line structure is considered a descrepancy
    :return:
    """

    # this function is way too long.. should be broken up to different functions.. but no time
    gs.clear_create_dir(p.discrep_tracker_output_dir)
    pf.print_step_separator("Discrepancy  Tracker")

    cmd = ih.get_input_enum_options('What would you like to do?', list(enums.DiscrepancyTrackerOptions))
    if cmd == enums.DiscrepancyTrackerOptions.FIND_AND_PROCCESS_DISCREPANCIES.value:

        pf.print_step_separator("Step 1: Enter and Analyze Tests")
        test_objs = ih.get_test_objs_from_excel()
        pf.print_note("Searching for file paths for each test...")
        passed_tests_with_paths = get_passed_tests_with_paths(test_objs)

        print("\n")
        pf.print_step_separator("Step 2: View Discrepancies and Other Results")
        pf.print_note("Ensuring that all tests have an ng file path with proper suffix (" + ap.ng_suffix + ")...")
        [num_tests_with_no_path_ng, passed_tests_with_path_and_ng_paths] = remove_tests_with_no_ng_path(
            passed_tests_with_paths)
        pf.print_warning(
            "Found " + str(num_tests_with_no_path_ng) + " tests marked as 'passed' or 'passed without code change', "
                                                        "but could not find the path to the new ng file!\nPlease ensure that that tests' ng paths are written as expected.\n"
                                                        "Wrote these tests to: " + tests_passed_missing_ng_path_text_path)

        pf.print_note("\nScanning for Discrepancies... (this might take 2 min...)")
        [num_files_with_discrepancies, num_files_no_discrepancies] = find_and_write_discrepancies(
            test_obj_list=passed_tests_with_path_and_ng_paths)

        # summary:
        pf.print_note("\n\nTotals tests analyzed (with correct ng path): " + str(
            num_files_with_discrepancies + num_files_no_discrepancies)
                      + "\nTests with descrepancies: " + str(num_files_with_discrepancies)
                      + "\nTests with no descrepances: " + str(num_files_no_discrepancies)
                      + "\n")
        pf.print_note("Wrote all discrepancies to: " + cur_discrepancy_csv_path)
        print(' ')

        sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(),
                            time=gs.get_time(), product=sfm.product_names.Discrepancy_Tracker.name, is_success=True,
                            tests_analyzed=(num_files_no_discrepancies + num_files_with_discrepancies),
                            total_files_with_descrepancies=num_files_with_discrepancies,
                            total_files_without_descrepancies=num_files_no_discrepancies,
                            passed_tests_with_no_ng_path=num_tests_with_no_path_ng)

    elif cmd == enums.DiscrepancyTrackerOptions.COMPARE_DISCREPANCIES.value:

        input_csv_dir_path = ih.get_input_ensure_valid(
            "Enter path to a directory containing all discrepancy CSVs.\n"
            "Make sure that directory:\n\t(1) does not contain any other files or directories!"
            "\n\t(2) contains files that are alphabetically ascending in order to process.\nEnter path:\n",
            os.path.isdir, "path does not lead to a valid directory!")
        pf.print_note("Processing discrepancies... please wait")
        gs.clear_create_dir(discrep_by_section_output_dir)
        [total_new_discreps, num_new_discrep_with_old_tests, num_new_discrep_with_new_tests] = (
            find_all_new_discrepancies(input_csv_dir_path))

        pf.print_note('Total new discrepancies: ' + str(total_new_discreps))
        pf.print_note('Number of new discrepancies, found in new tests added: ' + str(num_new_discrep_with_new_tests))
        pf.print_note('Number of new discrepancies, found in existing tests: ' + str(num_new_discrep_with_old_tests))

        sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(),
                            time=gs.get_time(), product=sfm.product_names.Discrepancy_Tracker.name, is_success=True,
                            files_with_new_descrepencies=num_new_discrep_with_old_tests,
                            tests_analyzed=total_new_discreps)

    else:
        print('error!')
        return


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
    fu.write_txt_to_file(tests_passed_missing_ng_path_text_path,
                         gs.open_list_as_string(str_of_all_tests_no_path_ng, ''))

    tests_with_path_ng = [test for test in test_obj_list if test.test_path_ng != cons.empty_char]
    return [num_tests_no_path_ng, tests_with_path_ng]


def find_and_write_discrepancies(test_obj_list):
    num_files_with_discrepancies = 0
    num_files_no_discrepancies = 0

    test_objs_with_discrepancies = []
    for test in (test_obj_list):
        if test.test_name == "EDIPOLLevelChargesAndAssociatedVAT_DoNotProrateNG":
            dummy = 'g'
        discrepancies = compare_files_by_function(test.test_path, test.test_path_ng)
        if discrepancies:
            num_files_with_discrepancies += 1
            # pf.print_header(test.test_name)
            res = test.test_name + ":\n"
            res += get_discrepancies_str_by_function(discrepancies,
                                                     src1_name=os.path.splitext(os.path.basename(test.test_path))[0],
                                                     src2_name=os.path.splitext(os.path.basename(test.test_path_ng))[0])
            res += '\n'
            test.discrepancy = res
            test_objs_with_discrepancies.append(test)
        else:
            test.discrepancy = cons.no_discrepancies_found
            test_objs_with_discrepancies.append(test)
            num_files_no_discrepancies += 1

    for test in test_objs_with_discrepancies:
        test.non_ng_content = fu.read_file_content_as_str(test.test_path)[0:max_char_count_allowed_by_pandas]
    cpo.create_csv_from_test_obj_list(test_objs_with_discrepancies, cur_discrepancy_csv_path)

    return [num_files_with_discrepancies, num_files_no_discrepancies]


def get_test_objs_with_path(test_objs):
    temp_csv_path = os.path.join(p.temp_dir, 'temp_copy.csv')
    cpo.create_csv_from_test_obj_list(test_objs, p.temp_csv_of_test_obj)
    cpo.write_paths_to_test_objs(p.temp_csv_of_test_obj, p.init_dict_file_name_to_path, temp_csv_path,
                                 ignore_warning=True)
    cpo.remove_tests_with_no_path(temp_csv_path, temp_csv_path)
    test_objs_with_path = cpo.create_test_obj_list_from_csv(temp_csv_path)
    return test_objs_with_path


def find_discrepancies_btw_2_csvs(INPUT_path_old_discrep_csv, INPUT_path_cur_discrep_csv,
                                  OUTPUT_new_tests_new_discreps_path, OUTPUT_old_tests_new_discreps_path):
    # INPUT_path_old_discrep_csv = ih.get_input_ensure_valid('Enter path to old discrepancies CSV', fu.is_csv_file,
    #                                                   'Please enter a valid csv path!')
    # INPUT_path_cur_discrep_csv = ih.get_input_ensure_valid('Enter path to current discrepancies CSV', fu.is_csv_file,
    #                                                   'Please enter a valid csv path!')

    [total_new_discreps, num_new_discrep_with_old_tests, num_new_discrep_with_new_tests] \
        = cpo.write_new_discrepancies_to_csvs(old_csv_path=INPUT_path_old_discrep_csv,
                                              cur_csv_path=INPUT_path_cur_discrep_csv,
                                              old_test_new_discreps_path=OUTPUT_old_tests_new_discreps_path,
                                              new_tests_new_discreps_path=OUTPUT_new_tests_new_discreps_path)

    return [total_new_discreps, num_new_discrep_with_old_tests, num_new_discrep_with_new_tests]


def print_discreps_per_section_if_exist(input_csv):

    if fu.read_file_content_as_str(input_csv) == cons.empty_char:
        return

    existing_files = fu.get_files_from_dir_as_list(discrep_by_section_output_dir, fu.is_txt_file, " a text file")
    test_objs = cpo.create_test_obj_list_from_csv(input_csv)
    test_name_max_length = len(max([test.test_name for test in test_objs], key=len))
    for test in test_objs:
        discrep_str = '\n\n' + tcf.get_test_discrep_nice_str(test, max_space=test_name_max_length)
        if discrep_str.__contains__(cons.could_not_locate_function):
            continue  # not ideal... but will be fine
        path_to_section_discrepancies = get_output_path_per_section(test.test_section)
        if path_to_section_discrepancies not in existing_files:
            existing_files.append(path_to_section_discrepancies)
            content_to_write = f"""New Discrepancies found in {test.test_section}:
            Note: Not always accurate.
            {discrep_str}"""
            fu.write_txt_to_file(path=get_output_path_per_section(test.test_section),
                                 content=content_to_write)
        else:
            fu.append_txt_to_file(content=discrep_str, path=path_to_section_discrepancies)


def get_output_path_per_section(section):
    return os.path.join(discrep_by_section_output_dir, 'new_discrepancies_' + section + '_' + gs.get_date() + '.txt')


def get_java_functions(file_content):
    # Regular expression to match Java functions
    pattern = re.compile(r'\b(?:public|private|protected|static|\s)+\w+\s+\w+\([^)]*\)\s*{')
    matches = pattern.finditer(file_content)
    functions = []
    for match in matches:
        functions.append(match.group())
    return functions


def compare_files_by_function(file_path1, file_path2, content1=cons.empty_char,
                              src1_name=cons.empty_char, src2_name=cons.empty_char):
    if content1 == cons.empty_char:
        content1 = fu.read_file_content_as_str(file_path1)
    content2 = fu.read_file_content_as_str(file_path2)
    functions1 = get_java_functions(content1)
    functions2 = get_java_functions(content2)

    if src1_name == cons.empty_char:
        src1_name = os.path.splitext(os.path.basename(file_path1))[0]
    if src2_name == cons.empty_char:
        src2_name = os.path.splitext(os.path.basename(file_path2))[0]

    discrepancies_by_function = {}

    function_set = sorted(set(functions1 + functions2))

    for function in function_set:
        num_close_brackets = get_num_closing_brackets(function, content1)

        pattern = re.escape(function) + r'[^}]*?\}' * num_close_brackets

        lines1 = re.search(pattern, content1, re.DOTALL)
        lines2 = re.search(pattern, content2, re.DOTALL)

        if lines1 and lines2:
            lines1 = lines1.group().strip()
            lines2 = lines2.group().strip()

            lines1_no_whitespace = re.sub(r'\s+', '', lines1)
            lines2_no_whitespace = re.sub(r'\s+', '', lines2)

            if lines1_no_whitespace != lines2_no_whitespace:
                discrepancies_by_function[function] = {
                    src1_name: lines1,
                    src2_name: lines2
                }

    return discrepancies_by_function


def get_discrepancies_str_by_function(discrepancies_by_function, src1_name, src2_name):
    if not discrepancies_by_function:
        return "No discrepancies found."
    else:
        res = ''
        for function, discrepancy in discrepancies_by_function.items():
            res += f"\nFunction: {function}"
            res += get_string_diff(str(discrepancy[src1_name]), str(discrepancy[src2_name]) + "\n")
        return res


def get_num_closing_brackets(function_header, content):
    """
    :param function_header: looks like: 'private void initParams() {'
    :return: gets the number of closing brackets expecting after this function header
    """
    res = 1  # function header includes a '{'
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


def get_changes_in_non_ng_files(input_path, output_path):
    src1_name = 'old_non_ng_content'
    src2_name = 'new_non_ng_content'

    test_objs = cpo.create_test_obj_list_from_csv(csv_path=input_path, from_cur_suffix=True)

    # in case test path changed - update test patht to current path to read content
    test_objs = [tcf.reassign_paths_if_corrupted(test_obj) for test_obj in test_objs]

    # set the test's discrepancy to discrepancy between old content and new content (of non ng files)
    for test_obj in test_objs:
        discrepancies_by_function = compare_files_by_function('-', test_obj.test_path, content1=test_obj.non_ng_content,
                                                              src1_name=src1_name, src2_name=src2_name)
        discrep_str = get_discrepancies_str_by_function(discrepancies_by_function, src1_name, src2_name) + '\n\n'
        test_obj.discrepancy = discrep_str

    if len(test_objs) > 0:
        cpo.create_csv_from_test_obj_list(test_obj_list=test_objs, path=output_path)


def find_all_new_discrepancies(input_csv_dir_path):
    total_new_discreps = 0
    num_new_discrep_with_old_tests = 0
    num_new_discrep_with_new_tests = 0

    file_path_list = fu.get_files_from_dir_as_list(input_csv_dir_path, fu.is_csv_file, " a csv file")
    file_path_list = sorted(file_path_list)
    for i in range(len(file_path_list) - 1):
        [temp_total_new_discreps, temp_num_new_discrep_with_old_tests, temp_num_new_discrep_with_new_tests] = (
            find_discrepancies_btw_2_csvs(
                INPUT_path_old_discrep_csv=file_path_list[i], INPUT_path_cur_discrep_csv=file_path_list[i + 1],
                OUTPUT_new_tests_new_discreps_path=new_tests_new_discreps_csv_path,
                OUTPUT_old_tests_new_discreps_path=old_tests_new_discreps_csv_path))

        get_changes_in_non_ng_files(input_path=old_tests_new_discreps_csv_path,
                                    output_path=changes_in_non_ng_files_csv_path)
        print_discreps_per_section_if_exist(input_csv=changes_in_non_ng_files_csv_path)

        total_new_discreps += temp_total_new_discreps
        num_new_discrep_with_old_tests += temp_num_new_discrep_with_old_tests
        num_new_discrep_with_new_tests += temp_num_new_discrep_with_new_tests

    pf.print_note('Printed discrepancies (between content of old and new non ng files) by section in directory:\n\t'
                  + discrep_by_section_output_dir)
    return [total_new_discreps, num_new_discrep_with_old_tests, num_new_discrep_with_new_tests]


if __name__ == '__main__':
    main_script()
