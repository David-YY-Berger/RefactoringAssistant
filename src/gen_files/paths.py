import os

# must change this to relative path! when do sync with intelliJ
testng_dir_orig = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\resources"
all_tests_dir = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\java\\tests"

# these can stay this way
testng_server_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testng_servers.csv")
cur_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cur_dir, "..", "..", "output")
ng_tests_dir_path = os.path.join(output_dir, "tests_containing_ng.txt")
non_ng_tests_dir_path = os.path.join(output_dir, "tests_do_not_contain_ng.txt")
temp_dict_test_name_to_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "temp", 'temp_dict_test_name_to_path.csv')
temp_dict_testng_to_test_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "temp", 'temp_dict_testng_to_test_name.csv')
