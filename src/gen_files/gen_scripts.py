import os
import mmap
import shutil

from src import application_properties as ap
from src.gen_files import paths as p, constants as cons, file_utils as fu

rec_test_path_list = []
dict_key_header = "test_name"
dict_val_header = "test_path"


def get_paths_from_dir(src_dir):
    global rec_test_path_list
    rec_test_path_list= []
    priv_rec_get_paths_from_dir(src_dir)
    return rec_test_path_list


def space_nicely(str1, max_length_str1, str2):
    spaces_to_add = ' ' * (max_length_str1 - len(str1))
    return str1 + spaces_to_add + str2


def open_list_as_string(lst, separator=" "):
    res = ""
    for s in lst:
        res += s + separator
    return res


def priv_rec_get_paths_from_dir(src_dir):
    global rec_test_path_list
    for f_name in os.listdir(src_dir):
        f_path = os.path.join(src_dir, f_name)
        if os.path.isfile(f_path):
            rec_test_path_list.append(f_path)
        if os.path.isdir(f_path):
            priv_rec_get_paths_from_dir(os.path.join(src_dir, f_path))


def get_names_from_paths(file_paths):
    return [os.path.splitext(os.path.basename(path))[0] for path in file_paths]

def get_paths_from_test_names(lst_test_names):
    with open(p.temp_dict_test_name_to_path, 'w') as file:
        file.write(dict_key_header + "," + dict_val_header + "\n")
    priv_rec_fill_dict(p.all_tests_dir)
    tests_not_found = []
    lst_test_paths = []
    for test_name in lst_test_names:
        test_name = (os.path.splitext(test_name)[0])
        # test_name = test_name.lower();
        test_path = fu.get_val_from_key_csv(csv_path=p.temp_dict_test_name_to_path, key_header=dict_key_header,
                                            val_header=dict_val_header, key=test_name)
        if test_path == cons.not_found:
            tests_not_found.append(test_name)
        else:
            lst_test_paths.append(test_path)

    if len(tests_not_found) > 0:
        print("\nThese tests were not found in our project (check for typos, ensure spelling matches project code..."
              "Update the Excel sheet, but do not change the code!):")
        for i in tests_not_found:
            print(i)
        print("\n")

    return lst_test_paths


def priv_rec_fill_dict(src_dir):
    with open(p.temp_dict_test_name_to_path, 'a') as temp_dict:
        for f_name in os.listdir(src_dir):
            f_path = os.path.join(src_dir, f_name)
            if os.path.isfile(f_path):
                f_name = f_name[: -len(cons.java_ext)]
                # f_name = f_name.lower()
                temp_dict.write(f_name + "," + f_path + "\n")
            if os.path.isdir(f_path):
                priv_rec_fill_dict(os.path.join(src_dir, f_path))


def build_ng_path(original_path):
    directories, file_name = os.path.split(original_path)
    directories = directories.split(os.path.sep)
    start = directories.index(ap.tests_dir_name) + 1
    root_directory = directories[0] + os.path.sep if directories[0] else ''
    modified_directories = [directory + ap.ng_suffix if index >= start else directory for index, directory in enumerate(directories)]
    modified_directories[0] = root_directory # fix the root directory (it keeps getting messed up..)
    modified_path = os.path.join(*modified_directories, file_name.replace(ap.file_ext, ap.ng_suffix + ap.file_ext))

    return modified_path


def clear_create_dir(this_dir):
    try:
        shutil.rmtree(this_dir)
    except FileNotFoundError:
        foo = '' # ignore if file not found
    except Exception as e:
        print(f"An error occurred: {e}")
    os.makedirs(this_dir)
