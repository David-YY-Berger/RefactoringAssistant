import sys
import os
import traceback

import src.gen_files.create_data_files
from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih
from src.gen_files import enums as enums, paths as p, gen_scripts as gs, stats_for_metrics as sfm
from src.refactor_tests import main_refactor_tests as mrt
from src.test_list_compare import main_test_list_compare as mtlc
from src.discreancy_tracker import main_discrepancy_tracker as mdt
from src.gen_files.ConsoleHelpers.print_functions import TextColors as tc
from src import application_properties as ap

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)

# to compile, use (venv) PS C:\RefactoringAssistant\RefactoringAssistantCode> pyinstaller C:\RefactoringAssistant\RefactoringAssistantCode\main-RefactoringAssistant.spec


def main_script():
    init_params()

    notes = ['Ensure that all file paths are ' + tc.UNDERLINE + "Absolute (not relative)" + tc.END + tc.NOTE_COLOR
             + ' and contain ' + tc.UNDERLINE + "only english letters" + tc.END + ". ",
             'This program assumes that all test files are java files without errors',
             'Remember to Sync your test directory\n',

             'Reading test directory from:\n\t\t' + p.test_project_base_txt_file_path,
             'Temporary maps:\n\t\t' + p.temp_dir,
             'Output:\n\t\t' + p.output_dir,
             'Custom Configuration file (to adjust keywords):\n\t\t' + p.path_local_custom_config + '\n',
             'We are open to feedback! If you have an idea - please share it']

    while True:
        pf.print_box("Refactoring Assistant", bold=True)
        pf.print_centered("Created by Ex Libris Automation")
        pf.print_centered("Version: " + ap.version)
        print(" ")
        pf.print_things_to_remember(notes)

        cmd = ih.get_input_enum_options("What would you like to do?", enums.MainOptions)

        if cmd == enums.MainOptions.REFACTOR_TESTS.value:
            try:
                mrt.main_script()
            except Exception as e:
                gs.report_error(product_name=sfm.product_names.Refactor_Tests.name, e=e)
        elif cmd == enums.MainOptions.DISCREPANCY_TRACKER.value:
            try:
                mdt.main_script()
            except Exception as e:
                gs.report_error(product_name=sfm.product_names.Discrepancy_Tracker.name, e=e)
        elif cmd == enums.MainOptions.TEST_LIST_COMPARE.value:
            try:
                mtlc.main_script()
            except Exception as e:
                gs.report_error(product_name=sfm.product_names.Test_List_Compare.name, e=e)
        # elif cmd == enums.MainOptions.LOGIN_AS_ADMIN.value:
        #     print("Coming soon")
        elif cmd == enums.MainOptions.SETUP.value:
            print("Coming soon")
            sfm.flag_ignore_david = False
        elif cmd == enums.MainOptions.EXIT.value:
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please choose a valid option.")


def init_params():

    files_created = False
    while not files_created:
        try:
            src.gen_files.create_data_files.init_maps_and_config()
            files_created = True
        except FileExistsError:
            pf.print_warning('Could not delete and recreate ' + p.temp_dir + '\n' +
                  'Please close any open files in that directory.\n' +
                  'When you are finished, enter any key to continue')
            input('')


if __name__ == '__main__':
    main_script()




