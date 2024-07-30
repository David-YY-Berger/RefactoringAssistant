import difflib
import errno
import os
import shutil
import pandas as pd
import getpass
import traceback
from datetime import datetime
from src.gen_files import paths as p, stats_for_metrics as sfm
from src.gen_files.ConsoleHelpers import print_functions as pf
from src import application_properties as ap


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
    pf.print_note("Clearing files in " + this_dir)
    # input("Clearing directory " + this_dir + " and files, ok? Press any key to continue")
    try:
        shutil.rmtree(this_dir)
    except FileNotFoundError as e:
        foo = '' # ignore if file not found
    except Exception as e:
        print(f"An error occurred: {e}")
    os.makedirs(this_dir)


def get_all_test_names_in_testng_files():
    csv_path = p.init_dict_testng_to_test_name
    df = pd.read_csv(csv_path, delimiter=',')
    unique_test_names = df['test_name'].unique()
    return unique_test_names


def report_error(product_name, e):
    error_msg = 'An Error occured: ' + str(e)
    error_msg += '\nTraceback:\n' + traceback.format_exc()
    sfm.append_to_stats(version=ap.version, user_name=get_cur_user_name(), date=get_date(),
                        time=get_time(), product=product_name, is_success=False,
                        error_msg=error_msg)
    print(error_msg)


def get_string_diff(str1, str2):
    d = difflib.Differ()
    diff = list(d.compare(str1.splitlines(), str2.splitlines()))
    res = ""
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            res += line + "\n"
    return res


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied: Unable to delete file '{file_path}'.")


def is_valid_integer(input_str):
    try:
        # Try converting the input string to an integer
        int(input_str)
        return True
    except ValueError:
        # If conversion fails, return False
        return False


def is_integer_in_range(value, min_val, max_val):
    # Check if the integer is within the specified range
    if min_val <= value <= max_val:
        return True
    else:
        return False
def add_suffix(s):
    # Find the index of the first '.'
    index = s.find('.')
    if index != -1:
        # Create the new string by slicing up to the index and adding 'AT'
        new_string = s[:index] + ap.ng_suffix
    else:
        # If there is no '.', return the original string
        new_string = s + ap.ng_suffix
    return new_string