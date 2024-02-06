import os
import shutil
import pandas as pd
import getpass
from datetime import datetime
from src.gen_files import paths as p


rec_test_path_list = []


def get_cur_user_name():
    return getpass.getuser()


def get_date():
    return datetime.now().strftime('%Y-%m-%d')


def get_time():
    return datetime.now().strftime('%H:%M:%S')


def trim_suffix(str):
    '''
    :param str:
    :return: removes char after the last '.'
    '''
    return os.path.basename(str).split('.')[0]


def get_paths_from_dir(src_dir):
    global rec_test_path_list
    rec_test_path_list= []
    priv_rec_get_paths_from_dir(src_dir)
    return rec_test_path_list


def priv_rec_get_paths_from_dir(src_dir):
    global rec_test_path_list
    for f_name in os.listdir(src_dir):
        f_path = os.path.join(src_dir, f_name)
        if os.path.isfile(f_path):
            rec_test_path_list.append(f_path)
        if os.path.isdir(f_path):
            priv_rec_get_paths_from_dir(os.path.join(src_dir, f_path))


def space_nicely(str1, max_length_str1, str2):
    spaces_to_add = ' ' * (max_length_str1 - len(str1))
    return str1 + spaces_to_add + str2


def open_list_as_string(lst, separator=" "):
    res = ""
    for s in lst:
        res += s + separator
    return res


def clear_create_dir(this_dir):
    try:
        shutil.rmtree(this_dir)
    except FileNotFoundError:
        foo = '' # ignore if file not found
    except Exception as e:
        print(f"An error occurred: {e}")
    os.makedirs(this_dir)


def get_all_test_names_in_testng_files():
    csv_path = p.init_dict_testng_to_test_name
    df = pd.read_csv(csv_path, delimiter=',')
    unique_test_names = df['test_name'].unique()
    return unique_test_names

