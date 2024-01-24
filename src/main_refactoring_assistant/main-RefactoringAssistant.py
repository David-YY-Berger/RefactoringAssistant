import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)

from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih
from src.gen_files import enums as enums, paths as p
from src.refactor_tests import main_refactor_tests as mrt
from src.gen_files.ConsoleHelpers.print_functions import TextColors as tc


notes = ['Ensure that all file paths and names contain ' + tc.UNDERLINE + "only english letters "
                    + tc.END + tc.NOTE_COLOR + "and " + tc.UNDERLINE + "no spaces" + tc.END,
         'Always use Absolute paths (not relative..)',
         'This program assumes that all test files are java files without errors',
         'The suffix, keywords, and other parameters can be adjusted in ' + p.application_properties_path,
         'We are open to feedback! If you have an idea - please share it']


def main_script():
    while True:
        pf.print_box("Refactoring Assistant", bold=True)
        pf.print_centered("Created by Ex Libris Automation")
        pf.print_things_to_remember(notes)


        cmd = ih.get_input_enum_options("What would you like to do?", enums.MainOptions)

        if cmd == enums.MainOptions.REFACTOR_TESTS.value:
            mrt.main_script()
        elif cmd == enums.MainOptions.RUN_DISCREPANCY_TRACKER.value:
            print("Coming soon")
        elif cmd == enums.MainOptions.LOGIN_AS_ADMIN.value:
            print("Coming soon: Login as admin...")
        elif cmd == enums.MainOptions.EXIT.value:
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please choose a valid option.")


if __name__ == '__main__':
    main_script()




