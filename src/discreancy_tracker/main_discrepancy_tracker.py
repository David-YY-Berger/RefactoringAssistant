# import difflib
# import os.path
# import sys
# import re
#
# import src.gen_files.test_class_funcs
# from src.gen_files import constants as cons, paths as p, gen_scripts as gs, file_utils as fu
# from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf
#
#
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
# sys.path.append(project_root)
#
# OLD_FILE = 0
# NG_FILE = 1
#
# def main_script():
#
#     num_files_w_ng = 0
#     num_files_wout_ng = 0
#     num_files_with_discrepancies = 0
#     pf.print_step_separator("Discrepancy  Tracker")
#     pf.print_step_separator("Step 1: Enter and Analyze Tests")
#     test_objs = ih.get_test_objs_from_input()
#     test_path_list = [test.test_path for test in test_objs]
#     for test_path in test_path_list:
#         pair = get_orig_and_ng(test_path)
#         if pair != cons.empty_char:
#             num_files_w_ng += 1
#             discrepancies = compare_files_by_function(pair[OLD_FILE], pair[NG_FILE])
#             if discrepancies:
#                 num_files_with_discrepancies += 1
#                 pf.print_header(os.path.splitext(os.path.basename(test_path))[0])
#                 print_discrepancies_by_function(discrepancies, os.path.splitext(os.path.basename(pair[OLD_FILE]))[0],
#                                                 os.path.splitext(os.path.basename(pair[NG_FILE]))[0])
#         else:
#             num_files_wout_ng += 1
#     pf.print_note("Found " + str(num_files_w_ng) + " tests with an ng version (of " + str(num_files_w_ng+ num_files_wout_ng) + " total tests). \n"
#                   + "Discrepancies found in " + str(num_files_with_discrepancies) + " files")
#
#
# def get_orig_and_ng(test_path):
#     ng_path = src.gen_files.test_name_to_path_funcs.build_ng_path(test_path)
#     ng_file_exists = os.path.isfile(ng_path)
#     if ng_file_exists:
#         return [test_path, ng_path]
#     else:
#         return cons.empty_char
#
#
# def get_java_functions(file_content):
#     # Regular expression to match Java functions
#     pattern = re.compile(r'\b(?:public|private|protected|static|\s)+\w+\s+\w+\([^)]*\)\s*{')
#     matches = pattern.finditer(file_content)
#     functions = []
#     for match in matches:
#         functions.append(match.group())
#     return functions
#
#
# def compare_files_by_function(file1, file2):
#
#     content1 = fu.read_file_content_as_str(file1)
#     content2 = fu.read_file_content_as_str(file2)
#     functions1 = get_java_functions(content1)
#     functions2 = get_java_functions(content2)
#
#     file_name1 = os.path.splitext(os.path.basename(file1))[0]
#     file_name2 = os.path.splitext(os.path.basename(file2))[0]
#
#     discrepancies_by_function = {}
#
#     for function in set(functions1 + functions2):
#         lines1 = re.search(re.escape(function) + r'.*?}', content1, re.DOTALL)
#         lines2 = re.search(re.escape(function) + r'.*?}', content2, re.DOTALL)
#
#         if lines1 and lines2:
#             lines1 = lines1.group().strip()
#             lines2 = lines2.group().strip()
#
#             if lines1 != lines2:
#                 discrepancies_by_function[function] = {
#                     file_name1: lines1,
#                     file_name2: lines2
#                 }
#
#     return discrepancies_by_function
#
#
# def print_discrepancies_by_function(discrepancies_by_function, file1_name, file2_name):
#     if not discrepancies_by_function:
#         print("No discrepancies found.")
#     else:
#         for function, discrepancy in discrepancies_by_function.items():
#             print(f"Function: {function}")
#             print(get_string_diff(str(discrepancy[file1_name]), str(discrepancy[file2_name]) + "\n"))
#
#
#
# def get_string_diff(str1, str2):
#     d = difflib.Differ()
#     diff = list(d.compare(str1.splitlines(), str2.splitlines()))
#     res = ""
#     for line in diff:
#         if line.startswith('- ') or line.startswith('+ '):
#             res += line + "\n"
#     return res
#
#
#
# if __name__ == '__main__':
#     main_script()
#
