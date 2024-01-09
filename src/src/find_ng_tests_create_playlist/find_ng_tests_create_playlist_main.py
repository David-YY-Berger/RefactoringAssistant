import mmap
import os
import sort_tests_to_files as sort_tests


src_dir = ng_dir = non_ng_dir =""
cur_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cur_dir, "..", "..", "output")

def main_script():
    init_params()
    sort_tests.sort_tests_to_files(src_dir=src_dir, ng_dir=ng_dir, non_ng_dir=non_ng_dir)
    # rec_sort_ng_tests(src_dir=src_dir)
    # write_tests_to_output(ng_dir=ng_dir, non_ng_dir=non_ng_dir)

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


# def get_server_for_test_path(test_path):
#     dir_to_search = "C:\\testFolder\\resources"
#     test = str(os.path.splitext(test_path)) + "\""  # add the quotation to make sure it's not a substring
#     for filename in os.listdir(dir_to_search):
#         f_path = os.path.join(dir_to_search, filename)
#         # checking if it is a file
#         if os.path.isfile(f_path):
#             with open(f_path, 'rb', 0) as file:  # 'rb' - binary mode. '0' - no buffer
#                 s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
#                 if s.find(test.encode()) != -1:
#                     print(test + ' found in file: ' + filename)
#                     return filename
#
#         if os.path.isdir(f_path):
#             # print("folder: " + f)
#             rec_sort_ng_tests(os.path.join(dir_to_search, f_path))
#     return test + " not found in any file!!"


if __name__ == '__main__':
    main_script()
