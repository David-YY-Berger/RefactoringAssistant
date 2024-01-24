from src.refactor_tests import create_playlist_from_files as cp, create_new_files as cnf, sort_tests_to_files as sttf
import src.application_properties as ap
import src.gen_files.enums
from src.gen_files import paths as p
from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf


def main_script():
    pf.print_step_separator("Source Compare")
    print("Source 1:")
    test_path = ih.get_tests_from_input()




if __name__ == '__main__':
    main_script()
