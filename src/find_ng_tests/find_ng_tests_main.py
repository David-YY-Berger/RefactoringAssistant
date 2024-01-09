import mmap
import os
from src import application_properties as ap
from src import file_utils as fu
import shutil

ng_cnt = 0
non_ng_cnt = 0
totalTests = 0
rec_ng_tests = []
rec_non_ng_tests = []
src_dir = ng_dir = non_ng_dir =""
cur_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cur_dir, "..", "..", "output")

def main_script():
    init_params()

    # test_path_list =
    rec_sort_ng_tests(src_dir=src_dir)
    write_tests_to_output(ng_dir=ng_dir, non_ng_dir=non_ng_dir)
    # print(str(totalTests - cnt) + " out of " + str(totalTests) + " do not contain the phrases")
    print("\n\n\n\n\n\n")
    #

    # for str in test_path_list:
    #     print(get_server_for_test_path(str))
    # ----------------------------------------- now, convert list of test paths to a playlist for automation player ---
    # test_suffix_list =  add_test_suffix_to_list(test_path_list)
    # create_playlist_from_test_list(test_suffix_list)


def init_params():
    global src_dir, cur_dir, ng_dir, non_ng_dir

    src_dir = input("enter source directory (where to take the tests to analyze)")
    # src_dir = "C:\\ScriptsForNGRefactoring\\rm"  # later get as param
    new_dir_path = os.path.join(output_dir, os.path.basename(src_dir))
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    ng_dir = os.path.join(output_dir, os.path.basename(src_dir), "ng_tests.txt")
    non_ng_dir = os.path.join(output_dir, os.path.basename(src_dir), "non_ng_tests.txt")


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


def add_test_suffix_to_list(lst):
    res = []
    for test_path in lst:
        for suffix_lst in get_test_suffix(test_path):
            res.append(suffix_lst)
    return res


def get_test_suffix(f_path):
    this_res = []
    with open(f_path, 'rb', 0) as file:  # 'rb' - binary mode. '0' - no buffer
        s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find("void test1()".encode()) != -1:
            for i in range(10):
                if s.find(str("void test" + str(i + 1) + "()").encode()) != -1:
                    this_res.append(os.path.basename(f_path) + "#test" + str(i + 1))
                else:
                    break
        elif s.find("void Test1()".encode()) != -1:
            for i in range(10):
                if s.find(str("void Test" + str(i + 1) + "()").encode()) != -1:
                    this_res.append(os.path.basename(f_path) + "#Test" + str(i + 1))
                else:
                    break
        else:
            this_res.append(os.path.basename(f_path) + "#test")
    return this_res


def create_playlist_from_test_list(test_suffix_list):
    text_file_path = "playlist.xml"
    xml_content = '''<java version="1.8.0_371" class="java.beans.XMLDecoder">
        <object class="java.util.Vector">
        '''
    for test_and_suffix in test_suffix_list:
        xml_content += ("<void method=\"add\">\n" +
                        "<string>" + test_and_suffix + "</string>\n" +
                        "</void>\n")

    xml_content += "</object>\n" + "</java>\n"
    with open(text_file_path, 'w') as file:
        file.write(xml_content)
    print(text_file_path + " has been created and written to.")


def get_server_for_test_path(test_path):
    dir_to_search = "C:\\testFolder\\resources"
    test = str(os.path.splitext(test_path)) + "\""  # add the quotation to make sure it's not a substring
    for filename in os.listdir(dir_to_search):
        f_path = os.path.join(dir_to_search, filename)
        # checking if it is a file
        if os.path.isfile(f_path):
            with open(f_path, 'rb', 0) as file:  # 'rb' - binary mode. '0' - no buffer
                s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                if s.find(test.encode()) != -1:
                    print(test + ' found in file: ' + filename)
                    return filename

        if os.path.isdir(f_path):
            # print("folder: " + f)
            rec_sort_ng_tests(os.path.join(dir_to_search, f_path))
    return test + " not found in any file!!"


if __name__ == '__main__':
    main_script()
