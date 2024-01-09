import mmap
import os
import sort_tests_to_files as sort_tests
import create_playlist_from_files as cp


src_dir = ng_path = non_ng_path = new_dir_path_in_output = ""
cur_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cur_dir, "..", "..", "output")

def main_script():
    init_params()
    sort_tests.public_sort_tests_to_files(src_dir=src_dir, ng_path=ng_path, non_ng_path=non_ng_path)
    cp.public_create_playlist_from_files(new_dir_path_in_output, non_ng_tests_path=non_ng_path)

def init_params():
    global src_dir, cur_dir, ng_path, non_ng_path, new_dir_path_in_output

    # src_dir = input("Enter source directory (where to take the tests to analyze)")
    src_dir = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\java\\tests\\rm"  # later get as param
    new_dir_path_in_output = os.path.join(output_dir, os.path.basename(src_dir))
    if not os.path.exists(new_dir_path_in_output):
        os.makedirs(new_dir_path_in_output)
    ng_path = os.path.join(output_dir, os.path.basename(src_dir), "ng_tests.txt")
    non_ng_path = os.path.join(output_dir, os.path.basename(src_dir), "non_ng_tests.txt")

if __name__ == '__main__':
    main_script()
