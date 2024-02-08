import os
from shutil import copyfile
import re

import src.gen_files
import src.gen_files.test_class_funcs
from src import application_properties as ap
from src.gen_files import file_utils as fu, test_class_funcs as tcf
from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih

files_created = 0
files_not_created = 0
base_names_or_imports_to_refactor = set()


def reset_global_params():
    global files_not_created
    global files_created
    global base_names_or_imports_to_refactor
    files_created = 0
    files_not_created = 0
    base_names_or_imports_to_refactor = set()


def create_version_w_ng_suffix_of_all_tests(test_path_list):

    test_path_list = sorted(test_path_list)
    for test_path in test_path_list:
        create_ng_file(test_path)
    pf.print_note("Created " + str(files_created) + " new files, found " + str(files_not_created) + " existing files")
    pf.print_note("Reminder to 'Rebuild' the test project to make sure there are no issues\n")
    return files_created


def create_ng_file(test_path, overwrite = False):
    try:
        global files_created
        global files_not_created
        global base_names_or_imports_to_refactor
        dest_path = tcf.get_ng_path_from_orig(test_path)

        if not overwrite:
            if not os.path.exists(dest_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                copyfile(test_path, dest_path)
                files_created += 1
                write_refactored_content(dest_path)
                pf.print_note("Created: " + dest_path)
            else:
                files_not_created += 1
        else:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            copyfile(test_path, dest_path)
            files_created += 1
            write_refactored_content(dest_path)
            pf.print_note("Created: " + dest_path)

    except IOError as e:
        print(f"Unable to copy file. {e}")


def write_refactored_content(dest_path):
    content = fu.read_file_content_as_str(dest_path)
    suffix = ap.ng_suffix
    class_name = os.path.splitext(os.path.basename(dest_path))[0][:-len(suffix)]
    class_name_and_suffix = class_name + suffix

    content = re.sub(r'package\s+tests(\.\w+)+;',
                    generate_package_header(dest_path), content, flags=re.UNICODE)

    # refactor class declaration - with and without 'extends'
    content = re.sub(rf'\s+class\s+{re.escape(class_name)}\s+extends\s+(\w+)\s*{{', rf' class {class_name_and_suffix} extends \1 {{', content, flags=re.UNICODE)
    content = re.sub(rf'\s+class\s+{re.escape(class_name)}\s+{{', rf' class {class_name_and_suffix} {{', content, flags=re.UNICODE)

    # refactor base name
    this_base_name = get_base_name_from_path(dest_path)
    if this_base_name in base_names_or_imports_to_refactor:
        content = re.sub(r'\s+class\s+(\w+)\s+extends\s+(\w+)\s*{', rf' class \1 extends \2{suffix} {{', content, flags=re.UNICODE)

    # refactor import statement
    imported_classes = get_imported_class_names(dest_path)
    for import_class_name in imported_classes:
        if import_class_name in base_names_or_imports_to_refactor:
            content = re.sub(rf'import\s+tests(?!\.super)(\.{import_class_name})+;', lambda match: match.group(0)
                             .replace('.', suffix + '.').replace(';', suffix + ';'), content, flags=re.UNICODE)
            content = re.sub(rf'import\s+tests' + ap.ng_suffix, lambda match: match.group(0)
                             .replace(f'tests{suffix}', 'tests'), content, flags=re.UNICODE)

    fu.write_txt_to_file(dest_path, content)


def get_base_name_from_path(dest_path):
    content = fu.read_file_content_as_str(dest_path)
    english_chars_pattern = re.compile(r'[^\x00-\x7F]+', flags=re.UNICODE)
    # Remove non-English characters from the input string
    only_eng_content = english_chars_pattern.sub('', content)

    class_declaration_pattern = re.compile(r'\s+class\s+(\w+)\s+extends\s+(\w+)\s*{', flags=re.UNICODE)
    match = class_declaration_pattern.search(only_eng_content)
    if match:
        base_name = match.group(2)
        return base_name
    else:
        return None


def get_imported_class_names(file_path):
    content = fu.read_file_content_as_str(file_path)
    pattern = r'import tests\.(?!supers\.)(.*?)\;'
    matches = re.findall(pattern, content, re.UNICODE)
    last_words = []
    for match in matches:
        words = match.split('.')
        last_word = words[-1].strip()
        last_words.append(last_word)
    return last_words


def get_directories_from_path(path, begin_dir = 'C:'):
    dir_path = os.path.dirname(path)
    normalized_path = os.path.normpath(dir_path)
    directories = normalized_path.split(os.path.sep)
    tests_index = directories.index(begin_dir) if begin_dir in directories else -1
    if tests_index != -1:
        return directories[tests_index:]
    else:
        return []


def generate_package_header(file_path):
    package_header = "package "
    dirs = get_directories_from_path(file_path, ap.tests_dir_name)
    for this_dir in dirs:
        package_header += this_dir + '.'
    last_dot = package_header.rfind('.')
    package_header = package_header[:last_dot] + ';'

    return package_header


def add_base_tests_if_prompted(test_path_list):
    global base_names_or_imports_to_refactor

    for path in test_path_list:
        base_names_or_imports_to_refactor.add(get_base_name_from_path(path))
        base_names_or_imports_to_refactor = base_names_or_imports_to_refactor.union(get_imported_class_names(path))
    for name in ap.test_base_names_to_ignore:
        base_names_or_imports_to_refactor.discard(name)
    base_names_or_imports_to_refactor.discard(None)
    if len(base_names_or_imports_to_refactor) > 0:
        base_names_or_imports_to_refactor = ih.get_chosen_items_from_list(init_prompt="Discovered base names and imported names.",
                                                          enter_list_prompt="Enter the numbers of the base names/imported names that you would like to include. ",
                                                          option_list=list(base_names_or_imports_to_refactor))
    if len(base_names_or_imports_to_refactor)>0:
        new_paths = src.gen_files.test_class_funcs.get_paths_from_test_names(base_names_or_imports_to_refactor)
        test_path_list += new_paths
    return test_path_list
