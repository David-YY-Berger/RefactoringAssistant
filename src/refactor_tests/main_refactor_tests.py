import os
import shutil

from src.refactor_tests import create_playlist_from_files as cp, create_new_test_files as cntf, sort_tests_to_files as sttf
import src.application_properties as ap
import src.gen_files.enums
from src.gen_files import paths as p, gen_scripts as gs, create_data_files as cf, stats_for_metrics as sfm
from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf


def main_script():
    init_params()
    pf.print_step_separator("Refactor Tests")
    pf.print_step_separator("Step 1: Enter and Analyze Tests")
    test_objs = ih.get_test_objs_from_input(get_test_paths_always=True)
    test_path_list = [test.test_path for test in test_objs]
    test_path_list = cntf.add_base_tests_if_prompted(test_path_list)
    if len(test_path_list) == 0 :
        print('no tests entered')
        return
    sttf.public_sort_tests_to_files(ng_path=p.ng_tests_dir_path, non_ng_path=p.non_ng_tests_dir_path,
                                          test_path_list=test_path_list)
    pf.print_step_separator("Step 2: Create new NG files (optional)")
    test_files_added = create_ng_tests_if_prompted(test_path_list=test_path_list)
    pf.print_step_separator("Step 3: Exporting playlist for non ng tests (to load to Automation Player)")
    cp.public_create_playlist_from_files(p.output_dir, non_ng_tests_path=p.non_ng_tests_dir_path)
    sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(), time=gs.get_time(),
                        product=sfm.product_names.Refactor_Tests.name, is_success=True, num_files_created=test_files_added)


def create_ng_tests_if_prompted(test_path_list):
    cmd = ih.get_input_enum_options("Would you like to create ng directories and files (with a " + ap.ng_suffix + " suffix)?\n"
                                    + "If the " + ap.ng_suffix + " test already exists, the program will not overwrite it.\n",
                                    list(src.gen_files.enums.OptionsYesNo),
                                    "Warning - cannot undo creating the files programmatically\n")
    files_created_here = 0
    if cmd == src.gen_files.enums.OptionsYesNo.YES.value:
        files_created_here = cntf.create_version_w_ng_suffix_of_all_tests(test_path_list)
    # elif cmd == cons.OptionsYesNo.NO.value:
    return files_created_here


def init_params():
    gs.clear_create_dir(p.output_dir)
    cntf.reset_global_params()
    cp.reset_global_params()


if __name__ == '__main__':
    main_script()
