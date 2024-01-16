import os
from shutil import copyfile
import re

from src import application_properties as ap
from src.gen_files import paths as p, file_utils as fu, input_helper as ih, gen_scripts as gs, constants as cons

files_created = 0
files_not_created = 0
base_names_or_imports_to_refactor = set()


def add_base_tests_if_prompted(test_path_list):
    global base_names_or_imports_to_refactor
    for path in test_path_list:
        base_names_or_imports_to_refactor.add(get_base_name_from_path(path))
        base_names_or_imports_to_refactor = base_names_or_imports_to_refactor.union(get_imported_class_names(path))
    for name in ap.test_base_names_to_ignore:
        base_names_or_imports_to_refactor.discard(name)
    base_names_or_imports_to_refactor.discard(None)
    if len(base_names_or_imports_to_refactor) > 0:
        base_names_or_imports_to_refactor = ih.get_chosen_items_from_list(init_prompt="Discovered the following base names/imported names:",
                                                          enter_list_prompt="Enter the numbers of the base names/imported names that you would like to refactor (and add the suffix to). ",
                                                          option_list=list(base_names_or_imports_to_refactor))
    if len(base_names_or_imports_to_refactor)>0:
        new_paths = gs.get_paths_from_test_names(base_names_or_imports_to_refactor)
        test_path_list += new_paths
    return test_path_list


def create_ng_versions_of_all_tests(test_path_list):

    for test_path in test_path_list:
        create_ng_file(test_path)
    print("Created " + str(files_created) + " new files, found " + str(files_not_created) + " existing files")
    print("Reminder to 'Rebuild' the test project to make sure there are no issues")


def create_ng_file(test_path):
    try:
        global files_created
        global files_not_created
        global base_names_or_imports_to_refactor
        dest_path = build_ng_path(test_path)

        if not os.path.exists(dest_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            copyfile(test_path, dest_path)
            files_created += 1
            write_refactored_content(dest_path)
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


def write_refactored_content(dest_path):
    content = fu.read_file_as_str(dest_path)
    suffix = ap.ng_suffix

    # refactor package
    content = re.sub(r'package\s+tests(\.\w+)+;',
                     lambda match: match.group(0).replace('.', suffix + '.').replace(';', suffix + ';'), content, flags=re.UNICODE)
    content = re.sub(r'package\s+tests' + ap.ng_suffix, lambda match: match.group(0).replace('tests' + suffix, 'tests'), content, flags=re.UNICODE)

    # refactor class declaration - with and without 'extends'
    content = re.sub(r'\s+class\s+(\w+)\s+extends\s+(\w+)\s*{', rf' class \1{suffix} extends \2 {{', content, flags=re.UNICODE)
    content = re.sub(r'\s+class\s+(\w+)\s+{', rf' class \1{suffix} {{', content, flags=re.UNICODE)

    # refactor base name
    this_base_name = get_base_name_from_path(dest_path)
    if this_base_name in base_names_or_imports_to_refactor:
        content = re.sub(r'\s+class\s+(\w+)\s+extends\s+(\w+)\s*{', rf' class \1 extends \2{suffix} {{', content, flags=re.UNICODE)

    # refactor import statement
    imported_classes = get_imported_class_names(dest_path)
    for class_name in imported_classes:
        if(class_name in base_names_or_imports_to_refactor):
            content = re.sub(r'import\s+tests(?!\.super)(\.\w+)+;', lambda match: match.group(0)
                             .replace('.', suffix + '.').replace(';', suffix + ';'), content, flags=re.UNICODE)
            content = re.sub(r'import\s+tests' + ap.ng_suffix, lambda match: match.group(0)
                             .replace('tests' + suffix, 'tests'),content, flags=re.UNICODE)

    fu.write_txt_to_file(dest_path, content)


def get_base_name_from_path(dest_path):
    content = fu.read_file_as_str(dest_path)
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
    content = fu.read_file_as_str(file_path)
    pattern = r'import tests\.(?!supers\.)(.*?)\;'
    matches = re.findall(pattern, content, re.UNICODE)
    last_words = []
    for match in matches:
        words = match.split('.')
        last_word = words[-1].strip()
        last_words.append(last_word)
    return last_words



