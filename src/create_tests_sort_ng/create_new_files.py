import os
from shutil import copyfile
import re

from src import application_properties as ap
from src.gen_files import paths as p, file_utils as fu, input_helper as ih, gen_scripts as gs

files_created = 0
files_not_created = 0


def create_ng_versions_of_all_tests(test_path_list):

    # print("\n\n\n\n\n")
    for test_path_list in test_path_list:
        test_base_names_set.add(get_base_name(test_path_list))

    for test_path in test_path_list:
        create_ng_file(test_path, do_package=True, do_class=True, do_base_name=False)
    print("Created " + str(files_created) + " new files, did not create " + str(files_not_created) + " existing files")
    refactor_base_names_if_prompted()

    # print("\n\n\n\n\n")


def refactor_base_names_if_prompted(test_base_names_set):
    for name in ap.test_base_names_to_ignore:
        test_base_names_set.discard(name)
    if len(test_base_names_set) > 0:
        chosen_base_names = ih.get_chosen_items_from_list(init_prompt="Discovered the following base names:",
                enter_list_prompt="Enter the numbers of the base names that you would like to refactor (and add the suffix to). ",
                option_list=list(test_base_names_set))
    if len(chosen_base_names)>0:
        path_list = gs.get_paths_from_test_names(chosen_base_names)
        for path in path_list:
            create_ng_file(path, do_package=False, do_class=False ,do_base_name=True)


def create_ng_file(test_path, do_package, do_class, do_base_name):
    try:
        global files_created
        global files_not_created
        global test_base_names_set
        dest_path = build_ng_path(test_path)

        if not os.path.exists(dest_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            copyfile(test_path, dest_path)
            files_created += 1
            refactor_package_class_or_basename(dest_path, do_package, do_class, do_base_name)
            test_base_names_set.add(get_base_name(dest_path))
        else:
            files_not_created += 1

    except IOError as e:
        print(f"Unable to copy file. {e}")


def build_ng_path(original_path):
    directories, file_name = os.path.split(original_path)
    directories = directories.split(os.path.sep)
    start = directories.index(ap.tests_dir_name) + 1
    root_directory = directories[0] + os.path.sep if directories[0] else ''
    modified_directories = [directory + ap.ng_suffix if index >= start else directory for index, directory in enumerate(directories)]
    modified_directories[0] = root_directory # fix the root directory (it keeps getting messed up..)
    modified_path = os.path.join(*modified_directories, file_name.replace(ap.file_ext, ap.ng_suffix + ap.file_ext))

    return modified_path


def refactor_package_class_or_basename(dest_path, do_package=False, do_class = False, do_base_name = False):
    content = fu.read_file_as_str(dest_path)
    suffix = ap.ng_suffix
    if do_package:
        content = re.sub(r'package\s+tests(\.\w+)+;',
                         lambda match: match.group(0).replace('.', suffix + '.').replace(';', suffix + ';'), content,
                         flags=re.UNICODE)
        content = re.sub(r'package\s+tests' + ap.ng_suffix, lambda match: match.group(0).replace('tests' + suffix, 'tests'),
                     content, flags=re.UNICODE)
    if do_class:
        content = re.sub(r'public\s+class\s+(\w+)\s+extends\s+(\w+)\s*{', rf'public class \1{suffix} extends \2 {{',
                         content, flags=re.UNICODE)
    if do_base_name:
        content = re.sub(r'public\s+class\s+(\w+)\s+extends\s+(\w+)\s*{', rf'public class \1 extends \2{suffix} {{',
                         content, flags=re.UNICODE)

    fu.write_txt_to_file(dest_path, content)



def get_base_name(dest_path):
    content = fu.read_file_as_str(dest_path)
    class_declaration_pattern = re.compile(r'\s*public\s+class\s+(\w+)\s+extends\s+(\w+)\s*{')
    match = class_declaration_pattern.search(content)
    if match:
        base_name = match.group(2)
        return base_name
    else:
        return None



