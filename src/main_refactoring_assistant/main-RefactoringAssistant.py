import sys
import os

from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih
from src.gen_files import enums as enums, paths as p
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
         'We are open to feedback! If you have an idea - please share it']


def main_script():
    while True:
        pf.print_box("Refactoring Assistant", bold=True)
        pf.print_centered("Created by Ex Libris Automation")
        pf.print_centered("Version: " + ap.version)
        print(" ")
        pf.print_things_to_remember(notes)

        # print(os.path.abspath(__file__))
        # print(os.path.abspath(sys.argv[0]))

        cmd = ih.get_input_enum_options("What would you like to do?", enums.MainOptions)

        if cmd == enums.MainOptions.REFACTOR_TESTS.value:
            mrt.main_script()
        elif cmd == enums.MainOptions.RUN_DISCREPANCY_TRACKER.value:
            print("Coming soon")
        elif cmd == enums.MainOptions.TEST_LIST_COMPARE.value:
            mtlc.main_script()
        elif cmd == enums.MainOptions.LOGIN_AS_ADMIN.value:
            print("Coming soon")
        elif cmd == enums.MainOptions.EXIT.value:
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please choose a valid option.")


if __name__ == '__main__':
    main_script()




