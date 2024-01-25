import os
import shutil

from src.refactor_tests import create_playlist_from_files as cp, create_new_files as cnf, sort_tests_to_files as sttf
import src.application_properties as ap
import src.gen_files.enums
from src.gen_files import paths as p, gen_scripts as gs, create_files as cf
from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf


def main_script():
    init_params()
    pf.print_step_separator("Refactor Tests")
    pf.print_step_separator("Step 1: Enter and Analyze Tests")
    test_path_list = ih.get_tests_from_input()
    sttf.public_sort_tests_to_files(ng_path=p.ng_tests_dir_path, non_ng_path=p.non_ng_tests_dir_path,
                                          test_path_list=test_path_list)
    pf.print_step_separator("Step 2: Create new NG files (optional)")
    create_ng_tests_if_prompted(test_path_list=test_path_list)
    pf.print_step_separator("Step 3: Exporting playlist for non ng tests (to load to Automation Player)")
    cp.public_create_playlist_from_files(p.output_dir, non_ng_tests_path=p.non_ng_tests_dir_path)


def create_ng_tests_if_prompted(test_path_list):
    cmd = ih.get_input_enum_options("Would you like to create ng directories and files (with a " + ap.ng_suffix + " suffix)?\n"
                                    + "If the " + ap.ng_suffix + " test already exists, the program will not overwrite it.\n"
                                    + "Warning - cannot undo creating the files programmatically\n",
                                    list(src.gen_files.enums.OptionsYesNo))
    if cmd == src.gen_files.enums.OptionsYesNo.YES.value:
        cnf.create_ng_versions_of_all_tests(test_path_list)
    # elif cmd == cons.OptionsYesNo.NO.value:


def init_params():
    gs.clear_create_dir(p.output_dir)
    gs.clear_create_dir(p.temp_dir)
    cf.create_testng_server_csv()
    cnf.reset_global_params()
    cp.reset_global_params()


if __name__ == '__main__':
    main_script()