import os

# fake directories:
# testng_dir_orig = "C:\\RefactoringAssistant\\RefactoringAssistantCode\\test_data\\src\\test\\resources"
# all_tests_dir = "C:\\RefactoringAssistant\\RefactoringAssistantCode\\test_data\\src\\test\\java\\tests"

cur_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'RefactoringAssistant')
output_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'RefactoringAssistant', 'output')
discrep_tracker_output_dir = os.path.join(output_dir, 'output_of_discrepancy_tracker')
temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'RefactoringAssistant', 'temp')

# these are assigned during runtime from the text file..
test_project_base_txt_file_path = os.path.join(main_dir, 'test_project_base_path.txt')
test_project_base_path = ''
testng_dir_orig = ''
all_tests_dir = ''


ng_tests_dir_path = os.path.join(output_dir, "tests_containing_ng.txt")
non_ng_tests_dir_path = os.path.join(output_dir, "tests_do_not_contain_ng.txt")


# temp maps creating at runtime from project, accessed program wide
test_name_header = 'test_name'
file_name_header = 'test_name'
testng_header = 'testng_file'
test_path_header = "test_path"
server_header = "server"
init_dict_file_name_to_path = os.path.join(temp_dir, 'init_dict_file_name_to_path.csv')
# init_dict_test_obj_from_testng = os.path.join(temp_dir, 'init_dict_test_obj_from_testng.csv')
init_dict_testng_to_test_name = os.path.join(temp_dir, 'init_dict_testng_to_test_name.csv')
temp_csv_of_test_obj = os.path.join(temp_dir, 'temp_test_obj_list.csv')

# temp map created from hardcoded string in file
testng_server_csv_path = os.path.join(temp_dir, "constant_testng_servers.csv")


# fix this:
# application_properties_path = os.path.join(cur_dir, "..", 'application_properties.py')


# be careful with these paths!!
# do not delete these files!!!
dir_sensitive_data  = r"Y:\QA\Automation\RefactoringAssistant\do_not_delete"
path_for_testng_server_src = os.path.join(dir_sensitive_data, 'src_testng_servers.csv')

dir_for_stats = os.path.join(dir_sensitive_data, 'dir_for_metric_stats')
path_for_stats = os.path.join(dir_for_stats, 'stats_for_metrics.csv')

dir_for_config_files = os.path.join(dir_sensitive_data, 'config_files')
path_for_default_config = os.path.join(dir_for_config_files, 'default_config.json')

dir_for_discrepancies = os.path.join(dir_sensitive_data, 'discrepancies')


#
