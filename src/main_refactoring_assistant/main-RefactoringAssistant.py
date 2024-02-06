import sys
import os

import src.gen_files.create_data_files
from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih
from src.gen_files import enums as enums, paths as p, gen_scripts as gs, stats_for_metrics as sfm
from src.refactor_tests import main_refactor_tests as mrt
from src.test_list_compare import main_test_list_compare as mtlc
from src.gen_files.ConsoleHelpers.print_functions import TextColors as tc
from src import application_properties as ap

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)


notes = ['Ensure that all file paths and names contain ' + tc.UNDERLINE + "only english letters"
                    + tc.END + tc.NOTE_COLOR + " and " + tc.UNDERLINE + "no spaces" + tc.END + ". ",
         'Always use Absolute paths (not relative..)',
         'This program assumes that all test files are java files without errors',
         'Remember to Sync your test directory. Test directory:  ' + p.all_tests_dir,
         "The suffix, keywords, and other parameters can be adjusted in 'Setup'",
         'Temporary maps can be found in: ' + p.temp_dir,
         'We are open to feedback! If you have an idea - please share it']


def main_script():
    init_params()
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
                sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(),
                                    time=gs.get_time(), product=sfm.product_names.Refactor_Tests.name, is_success=False, error_msg= f'error - {e}')
                print(f'Error - {e}')
        elif cmd == enums.MainOptions.RUN_DISCREPANCY_TRACKER.value:
            print("Coming soon")
        elif cmd == enums.MainOptions.TEST_LIST_COMPARE.value:
            try:
                mtlc.main_script()
            except Exception as e:
                sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(),
                                    time=gs.get_time(), product=sfm.product_names.Test_List_Compare.name, is_success=False, error_msg=str(e))
        # elif cmd == enums.MainOptions.LOGIN_AS_ADMIN.value:
        #     print("Coming soon")
        # elif cmd == enums.MainOptions.SETUP.value:
        #     print("Coming soon")
        elif cmd == enums.MainOptions.EXIT.value:
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please choose a valid option.")


def init_params():
    src.gen_files.create_data_files.init_maps()


if __name__ == '__main__':
    main_script()




