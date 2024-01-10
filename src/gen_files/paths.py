import os

# must change this to relative path! when do sync with intelliJ
testng_dir_orig = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\resources"
all_tests_dir = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\java\\tests"

# these can stay this way
testng_server_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testng_servers.csv")

