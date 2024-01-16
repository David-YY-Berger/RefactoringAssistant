import subprocess

from src.gen_files.ConsoleHelpers import print_functions as pf, input_helper as ih
from src.gen_files import enums as enums, paths as p


notes = ['This program assumes that all test files are java files without errors',
         'The suffix, and other parameters can be adjusted in ' + p.application_properties_path,
         'We are open to feedback! If you have an idea - please share it']


def main_script():
    while True:
        pf.print_box("Refactoring Assistant", bold=True)
        pf.print_centered("Created by Ex Libris Automation")
        pf.print_things_to_remember(notes)


        cmd = ih.get_input_enum_options("What would you like to do?", enums.MainOptions)

        if cmd == enums.MainOptions.REFACTOR_TESTS.value:
            try:
                subprocess.run(['python', p.refactor_tests_main], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running the script: {e}")
        elif cmd == enums.MainOptions.RUN_DISCREPANCY_TRACKER.value:
            # Implement the logic for RUN_DISCREPANCY_TRACKER
            print("Running discrepancy tracker...")
        elif cmd == enums.MainOptions.LOGIN_AS_ADMIN.value:
            print("Coming soon: Login as admin...")
        elif cmd == enums.MainOptions.EXIT.value:
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please choose a valid option.")


if __name__ == '__main__':
    main_script()




