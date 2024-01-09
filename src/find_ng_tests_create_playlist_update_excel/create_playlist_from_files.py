import os
import mmap
from src import constants as cons

from src import file_utils as fu

# must change this to relative path! when do sync with intelliJ
testng_dir_orig = "C:\\urm\\workspace-1.0.0.2-URM\\alma_itest_ux\\src\\test\\resources"
testng_server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",  "testng_servers.csv")

tests_not_in_testng = []
testng_files_set = set()


def public_create_playlist_from_files(dest_dir, non_ng_tests_path):

    # test_suffix_list =  priv_add_test_suffix_to_list(fu.read_lines_as_list_from_file(non_ng_tests_path))

    test_path_list = fu.read_lines_as_list_from_file(non_ng_tests_path)
    all_lsts = priv_get_lists_by_server(test_path_list)
    priv_create_all_playlists(all_lsts, dest_dir)


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
    priv_create_playlist_from_test_list(all_lists[cons.Servers.QAC01.value], dest_dir, cons.Servers.QAC01.name)
    priv_create_playlist_from_test_list(all_lists[cons.Servers.SQA_NA01.value], dest_dir, cons.Servers.SQA_NA01.name)
    priv_create_playlist_from_test_list(all_lists[cons.Servers.SQA_EU01.value], dest_dir, cons.Servers.SQA_EU01.name)
    priv_create_playlist_from_test_list(all_lists[cons.Servers.NOT_FIND_SERVER.value], dest_dir, cons.Servers.NOT_FIND_SERVER.name)

def priv_create_playlist_from_test_list(test_suffix_list, dest_dir, server_name):

    # here! change the funciton call..

    text_file_path = os.path.join(dest_dir, "playlist.xml")
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


def priv_rec_get_server_for_test_path(testng_dir, test_path):
    global tests_not_in_testng
    # run this in intelliJ and get the relative path there... testng_dir = input("Please enter the absolute path of the 'resources' directory which holds the 'testng' files")

    test_name = os.path.basename(test_path)[:-len(".java")] + "\""  # add the quotation to make sure it's not a substring
    for filename in os.listdir(testng_dir):
        f_path = os.path.join(testng_dir, filename)
        if os.path.isfile(f_path):
            with open(f_path, 'rb', 0) as file:
                s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                if s.find(test_name.encode()) != -1:
                    # print(test_name + ' found in file: ' + filename)
                    # testng_files_set.add(filename)
                    return fu.get_server_from_testng(csv_path=testng_server_path, testng_file_name=filename)

        if os.path.isdir(f_path):
            priv_rec_get_server_for_test_path(testng_dir = os.path.join(testng_dir, f_path), test_path=test_path)
    tests_not_in_testng.append(test_name) # not found in any testng file


def priv_get_lists_by_server(test_path_lst):
    res = [[] for _ in range(len(list(cons.Servers)))]

    for test_path in test_path_lst:
        server = priv_rec_get_server_for_test_path(test_path=test_path, testng_dir=testng_dir_orig)

        if server == cons.empty_csv:
            res[cons.Servers.NOT_FIND_SERVER.value].append(test_path)
        elif server == cons.Servers.QAC01.name:
            res[cons.Servers.QAC01.value].append(test_path)
        elif server == cons.Servers.SQA_NA01.name:
            res[cons.Servers.SQA_NA01.value].append(test_path)
        elif server == cons.Servers.SQA_EU01.name:
            res[cons.Servers.SQA_EU01.value].append(test_path)
        elif server == cons.not_found:
            print("testng file not in csv!")

    return res