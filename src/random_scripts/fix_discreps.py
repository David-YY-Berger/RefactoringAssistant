# import pandas as pd
#
#
# class Function:
#     def __init__(self, func_name, func_content):
#         self.func_name = func_name
#         self.func_content = func_content
#
#
# def parse_functions(input_string):
#     functions = []
#     lines = input_string.strip().split('\n')
#     current_function = None
#
#     for line in lines:
#         if line.startswith('Function:'):
#             if current_function is not None:
#                 functions.append(current_function)
#             func_name = line.split('Function: ')[1].split('(')[0].strip()
#             current_function = Function(func_name, "")
#         elif current_function is not None:
#             current_function.func_content += line.strip() + '\n'
#
#     if current_function is not None:
#         functions.append(current_function)
#
#     return sorted(functions, key=lambda x: x.func_name.lower())
#
#
# # Read CSV file into a DataFrame
# df = pd.read_csv(r"C:\Users\davidbe\Downloads\temp_old_tests_new_discreps_.csv")
# # Iterate over each row in the DataFrame
# for index, row in df.iterrows():
#
#     beg_str = '\n\n\t Test: ' + row['test_name']
#     print (beg_str)
#
#     # Read content of discrepancy_cur and discrepancy_old columns into variables
#     content_cur = row['discrepancy_cur']
#     content_old = row['discrepancy_old']
#     f_cur_list = parse_functions(content_cur)
#     f_old_list = parse_functions(content_old)
#
#     # Iterate over functions in f_cur_list
#     for cur_function in f_cur_list:
#         # Check if the current function exists in f_old_list
#         # printed_once = False
#         found_discrepancy = True
#         for old_function in f_old_list:
#             if cur_function.func_name == old_function.func_name and cur_function.func_content == old_function.func_content:
#                 found_discrepancy = False
#                 break
#
#         # If the current function is not found in f_old_list, it's a discrepancy
#         if found_discrepancy:
#             # if not printed_once:
#             #     printed_once = True
#             #     print(beg_str)
#             print('found discrepancy in function ' + cur_function.func_name)