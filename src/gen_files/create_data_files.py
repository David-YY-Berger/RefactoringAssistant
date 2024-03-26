import json
import os
import re

from src.gen_files import file_utils as fu, paths as p, gen_scripts as gs, test_class_funcs as tcf, \
    csv_pandas_ops as cpo, enums as enums, constants as cons
from src.gen_files.ConsoleHelpers import input_helper as ih
from src import application_properties as ap
import xml.etree.ElementTree as ET


def create_testng_server_csv():
    testng_server_content = gs.open_list_as_string(fu.read_lines_as_list_from_file(p.path_for_testng_server_src), '\n')
    fu.write_txt_to_file(p.testng_server_csv_path, testng_server_content)


def init_maps_and_config():
    gs.clear_create_dir(p.temp_dir)

    set_application_properties()

    if not os.path.exists(p.test_project_base_txt_file_path):
        with open(p.test_project_base_txt_file_path, 'w') as file:
            file.write(r'C:\urm\workspace-1.0.0.2-URM\alma_itest_ux\src\test')

    with open(p.test_project_base_txt_file_path, 'r') as file:
        p.test_project_base_path = file.read().strip()
    if not os.path.isdir(p.test_project_base_path):
        ih.reassign_project_path()

    p.testng_dir_orig = os.path.join(p.test_project_base_path, "resources")
    p.all_tests_dir = os.path.join(p.test_project_base_path, "java", "tests")

    create_testng_server_csv()
    fill_dict_file_name_to_path(p.all_tests_dir)
    fill_dict_testng_to_test_name(p.testng_dir_orig)
    # fill_dict_test_objs_from_testng(p.testng_dir_orig)


def fill_dict_testng_to_test_name(testng_dir):
    testng_files_paths = gs.get_paths_from_dir(testng_dir)

    with open(p.init_dict_testng_to_test_name, 'w') as file:
        file.write(p.test_name_header + "," + p.testng_header + "\n")

    with open(p.init_dict_testng_to_test_name, 'a') as temp_dict:
        for testng_file in testng_files_paths:
            test_names = get_test_names_from_testng_file(testng_file)
            for test_name in test_names:
                temp_dict.write(test_name + ',' + os.path.basename(testng_file) + "\n")


def get_class_name_from_testng_file(testng_file):
    class_names_list = []
    tree = ET.parse(testng_file)
    root = tree.getroot()

    for test_elem in root.findall(".//test"):
        for class_elem in test_elem.findall(".//class"):
            class_name = class_elem.get("name")
            if class_name:
                class_names_list.append(class_name)
    return class_names_list


def fill_dict_file_name_to_path(dir_with_tests):
    with open(p.init_dict_file_name_to_path, 'w') as file:
        file.write(p.file_name_header + "," + p.test_path_header + "\n")
    rec_fill_name_to_path_dict(dir_with_tests)


# def fill_dict_test_name_to_path_from_testng_files():
#     test_names = gs.get_all_test_names_in_testng_files()
#     test_obj_list = tcf.get_test_obj_list_w_path_from_name_list(test_names)
#     cpo.create_csv_from_test_obj_list(test_obj_list, p.init_dict_test_name_to_path)


def rec_fill_name_to_path_dict(src_dir):
    with open(p.init_dict_file_name_to_path, 'a') as temp_dict:
        for f_name in os.listdir(src_dir):
            f_path = os.path.join(src_dir, f_name)
            if os.path.isfile(f_path):
                f_name = gs.trim_suffix(f_name)
                # f_name = f_name.lower()
                temp_dict.write(f_name + "," + f_path + "\n")
            if os.path.isdir(f_path):
                rec_fill_name_to_path_dict(os.path.join(src_dir, f_path))


def get_test_names_from_testng_file(filepath):
    test_names = []

    tree = ET.parse(filepath)
    root = tree.getroot()

    for test_elem in root.findall(".//test"):
        for class_elem in test_elem.findall(".//class"):
            class_name = class_elem.get("name")
            if class_name:
                test_names.append(class_name)

    return [s.split('.')[-1] for s in test_names]


def init_application_properties_from_config(path_to_json_config):
    try:
        with open(path_to_json_config, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        # print(f"Couldn't find default config file at: {path_to_json_config}")
        return False
    except PermissionError:
        print(f"Couldn't access default config; maybe being used by another process!")
        return False

    ap.ng_suffix = json_data["ng_suffix"]
    ap.tests_dir_name = json_data["tests_dir_name"]
    ap.file_ext = json_data["file_ext"]
    ap.version = json_data["version"]

    ap.excel_row_of_column_header = json_data["excel_row_of_column_header"]
    ap.excel_column_with_tests_name = json_data["excel_column_with_tests_name"]
    ap.excel_column_with_result = json_data["excel_column_with_result"]
    ap.excel_result_passed = json_data["excel_result_passed"]
    ap.excel_result_passed_wo_code_change = json_data["excel_result_passed_wo_code_change"]

    ap.csv_column_with_section = json_data["csv_column_with_section"]
    ap.csv_column_with_test_name = json_data["csv_column_with_test_name"]
    ap.csv_column_with_type = json_data["csv_column_with_type"]
    ap.csv_all_column_headers = json_data["csv_all_column_headers"]

    ap.test_base_names_to_ignore = json_data["test_base_names_to_ignore"]

    ap.default_keywords_choice = json_data["default_keywords_choice"]
    ap.keywords1_name = json_data["keywords1_name"]
    ap.keywords1 = json_data["keywords1"]
    ap.keywords2_name = json_data["keywords2_name"]
    ap.keywords2 = json_data["keywords2"]

    return True


def set_application_properties():

    # initially - check if user had custom configs
    custom_config_is_different = False
    if os.path.exists(p.path_local_custom_config):
        content_custom_config = fu.read_file_content_as_str(p.path_local_custom_config)
        if os.path.exists(p.path_local_temp_default_config):
            local_default_config_content = fu.read_file_content_as_str(p.path_local_temp_default_config)
            if content_custom_config != local_default_config_content:
                custom_config_is_different = True
    #     if local default file doesn't exists, assume we can overwrite user's local config... don't have a better way of dealing with this
    else:
        content_custom_config = cons.empty_char

    # read default config from centralized location. overwrite local default config copy
    try:
        content_default_config = fu.read_file_content_as_str(p.path_for_default_config)
    except PermissionError:
        content_default_config = fu.read_file_content_as_str(p.path_for_default_config_if_first_is_open)
    except FileNotFoundError:
        content_default_config = fu.read_file_content_as_str(p.path_for_default_config_if_first_is_open)

    fu.write_txt_to_file(p.path_local_temp_default_config, content_default_config)

    # check if any custom configs exist
    chosen_config_file_path = p.path_local_temp_default_config
    if custom_config_is_different:
        cmd = ih.get_input_enum_options("\nDetected custom configurations. What would you like to do?",
                                        list(enums.CustomOrDefaultConfig),
                                        "Ensure that the variable names in your custom config file EXACTLY "
                                        "match the variables names in the default config file")
        if cmd == enums.CustomOrDefaultConfig.DEFAULT_CONFIG.value:
            foo = ''
            # chosen_config_file_path = p.path_local_temp_default_config
        elif cmd == enums.CustomOrDefaultConfig.CUSTOM_CONFIG.value:
            chosen_config_file_path = p.path_local_custom_config
        elif cmd == enums.CustomOrDefaultConfig.OVERWRITE_MY_CUSTOM_CONFIG_WITH_DEFULT.value:
            fu.write_txt_to_file(p.path_local_custom_config, content_default_config)
            chosen_config_file_path = p.path_local_temp_default_config
    else:
        fu.write_txt_to_file(p.path_local_custom_config, content_default_config)

    init_application_properties_from_config(chosen_config_file_path)

# def fill_dict_test_objs_from_testng(testng_dir_orig):
#
#     test_obj_list = []
#     testng_files_paths = gs.get_paths_from_dir(testng_dir_orig)
#     for testng_file_path in testng_files_paths:
#         class_names = get_class_name_from_testng_file(testng_file_path)
#         for class_name in class_names:
#             test_obj = tcf.get_test_obj_from_class_name(class_name)
#             test_obj.testng_file_name = os.path.basename(testng_file_path)
#             test_obj_list.append(test_obj)
#     cpo.create_csv_from_test_obj_list(test_obj_list=test_obj_list, path=p.init_dict_test_obj_from_testng)
