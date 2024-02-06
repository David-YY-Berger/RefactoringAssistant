import os

# must change this to relative path! when do sync with intelliJ
testng_dir_orig = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\resources"
all_tests_dir = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\java\\tests"

# fake directories:
# testng_dir_orig = "C:\\RefactoringAssistant\\RefactoringAssistantCode\\test_data\\src\\test\\resources"
# all_tests_dir = "C:\\RefactoringAssistant\\RefactoringAssistantCode\\test_data\\src\\test\\java\\tests"

cur_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'RefactoringAssistant', 'output')
temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'RefactoringAssistant', 'temp')

ng_tests_dir_path = os.path.join(output_dir, "tests_containing_ng.txt")
non_ng_tests_dir_path = os.path.join(output_dir, "tests_do_not_contain_ng.txt")

# temp maps creating at runtime from project
test_name_header = 'test_name'
file_name_header = 'file_name'
testng_header = 'testng_file'
test_path_header = "test_path"
server_header = "server"
init_dict_file_name_to_path = os.path.join(temp_dir, 'init_dict_file_name_to_path.csv')
init_dict_test_name_to_path = os.path.join(temp_dir, 'init_dict_test_name_to_path.csv')
init_dict_testng_to_test_name = os.path.join(temp_dir, 'init_dict_testng_to_test_name.csv')
temp_csv_of_test_obj = os.path.join(temp_dir, 'temp_test_obj_list.csv')

# temp map created from hardcoded string in file
testng_server_csv_path = os.path.join(temp_dir, "constant_testng_servers.csv")



# fix this:
application_properties_path = os.path.join(cur_dir, "..", 'application_properties.py')


