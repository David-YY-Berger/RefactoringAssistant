import csv
import os
import mmap
import re

import src.gen_files.enums as enums
from src.gen_files import constants as cons, file_utils as fu, paths as p, gen_scripts as gs
from src.gen_files.ConsoleHelpers import print_functions as pf

# testng_files_set = set() keep for debugging
testng_with_no_server = set()
tests_with_no_testng = set()


def reset_global_params():
    global tests_with_no_testng, testng_with_no_server
    tests_with_no_testng = set()
    testng_with_no_server = set()


def public_create_playlist_from_files(dest_dir, non_ng_tests_path):
    pf.print_note("Mapping tests to testng files and servers...please wait")
    test_path_list = fu.read_lines_as_list_from_file(non_ng_tests_path)
    all_lists_by_server = priv_get_lists_by_server(test_path_list)
    priv_create_all_playlists(all_lists_by_server, dest_dir)
    pf.print_note("Finished creating files")

    # keep for debugging
    # print("\n\n\n")
    # for i in sorted(testng_files_set):
    #     print(i)


def priv_add_test_suffix_to_list(lst):
    res = []
    for test_path in lst:
        for suffix_lst in priv_get_test_suffix(test_path):
            res.append(suffix_lst)
    return res


def priv_get_test_suffix(f_path):
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


def priv_create_all_playlists(all_lists, dest_dir):

    for i, lst in enumerate(all_lists):
        if len(lst) > 0:
            priv_create_playlist_from_test_list(lst, dest_dir, enums.get_name_from_value_enum(i, enum_class=enums.Servers))


def priv_create_playlist_from_test_list(test_suffix_list, dest_dir, server_name):

    if len(test_suffix_list) == 0:
        return
    text_file_path = os.path.join(dest_dir, "playlist_" + server_name + ".xml")
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
    pf.print_note("wrote " + str(len(test_suffix_list)) + " tests to " + text_file_path)


def priv_get_lists_by_server(test_path_lst):
    res = [[] for _ in range(len(list(enums.Servers)))]

    for test_path in test_path_lst:
        server = priv_get_server_for_test_path(test_path=test_path, testng_dir=p.testng_dir_orig)

        if server == cons.not_find_testng:
            tests_with_no_testng.add(os.path.splitext(os.path.basename(test_path))[0])
        elif server == cons.empty_char:
            res[enums.Servers.COULD_NOT_FIND_SERVER.value].append(test_path)
        else:
            for s in list(enums.Servers):
                if server == s.name:
                    res[s.value].append(test_path)

    if len(tests_with_no_testng) > 0:
        pf.print_warning("\nNo testng file contains the following tests (but they do exist in the project):\n" + gs.open_list_as_string(list(tests_with_no_testng), "\n") +
              "Please find out if that test should be added to a testng file. \n ")
            # "Choose a Server from: " + gs.open_list_as_string(list(s.name for s in src.gen_files.enums.Servers)) + "\n")
    if len(testng_with_no_server) > 0:
        pf.print_warning("\nNo server found for the following testng files:\n" + gs.open_list_as_string(list(testng_with_no_server), "\n") +
              "Please contact your admin to add the sever for these testng files\n")
            # "Choose a Server from: " + gs.open_list_as_string(list(s.name for s in src.gen_files.enums.Servers)) + "\n")
    return res


def priv_get_server_for_test_path(test_path, testng_dir):
    priv_fill_dict_testng_to_test_name(testng_dir)
    testname = os.path.splitext(os.path.basename(test_path))[0]
    testng_file = cons.empty_char
    with open(p.temp_dict_testng_to_test_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['test_name'] == testname:
                testng_file = row['testng_file']
    if testng_file == cons.empty_char:
        return cons.not_find_testng
    server = fu.get_server_from_testng(p.testng_server_csv_path, testng_file)
    if server == cons.empty_char:
        testng_with_no_server.add(testng_file)
    return server


def priv_fill_dict_testng_to_test_name(testng_dir):
    testng_files_paths = gs.get_paths_from_dir(testng_dir)
    test_name_header = 'test_name'
    testng_header = 'testng_file'

    with open(p.temp_dict_testng_to_test_name, 'w') as file:
        file.write(test_name_header + "," + testng_header + "\n")

    with open(p.temp_dict_testng_to_test_name, 'a') as temp_dict:
        for testng_file in testng_files_paths:
            test_names=priv_get_test_names_from_testng_file(testng_file)
            for test_name in test_names:
                temp_dict.write(test_name + ',' + os.path.basename(testng_file) + "\n")


def priv_get_test_names_from_testng_file(filepath):
    test_names = []

    with open(filepath, 'r') as file:
        content = file.read()
        class_name_pattern = re.compile(r'<class\s+name="([^"]+)"\s*/?>')
        matches = class_name_pattern.findall(content)
        test_names.extend(matches)

    return [s.split('.')[-1].replace('"', '') for s in test_names]




