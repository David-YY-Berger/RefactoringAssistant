import mmap
import os
from src import application_properties as ap
from src import file_utils as fu

ng_cnt = 0
non_ng_cnt = 0
totalTests = 0
rec_ng_tests = []
rec_non_ng_tests = []

def sort_tests_to_files(src_dir, ng_dir, non_ng_dir):
    rec_sort_ng_tests(src_dir=src_dir)
    write_tests_to_output(ng_dir=ng_dir, non_ng_dir=non_ng_dir)

def rec_sort_ng_tests(src_dir):
    global ng_cnt
    global non_ng_cnt
    global totalTests
    global rec_ng_tests
    global rec_non_ng_tests

    for filename in os.listdir(src_dir):
        f_path = os.path.join(src_dir, filename)
        if os.path.isfile(f_path):
            with open(f_path, 'rb', 0) as file:  # 'rb' - binary mode. '0' - no buffer
                s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                totalTests = totalTests + 1
                is_ng_test = False
                str_to_add = ""
                for word in ap.keywords:
                    if s.find(word.encode()) != -1:
                        str_to_add += " | " + word
                        is_ng_test = True
                if is_ng_test == False:
                    rec_non_ng_tests.append(f_path)
                    non_ng_cnt += 1
                else:
                    rec_ng_tests.append(os.path.basename(f_path) + str_to_add)
                    ng_cnt += 1

        if os.path.isdir(f_path):
            rec_sort_ng_tests(os.path.join(src_dir, f_path))


def write_tests_to_output(ng_dir, non_ng_dir):
    global ng_cnt
    global non_ng_cnt

    str_ng_tests = ""
    for s in rec_ng_tests:
        str_ng_tests += s + "\n"
    fu.write_to_txt_file(ng_dir, str_ng_tests)
    print("Wrote " + str(ng_cnt) + " tests to " + ng_dir)

    str_non_ng_tests = ""
    for s in rec_non_ng_tests:
        str_non_ng_tests += s + "\n"
    fu.write_to_txt_file(non_ng_dir, str_non_ng_tests)
    print("Wrote " + str(non_ng_cnt) + " tests to " + non_ng_dir)

    print("Total test analyzed: " + str(ng_cnt + non_ng_cnt))

