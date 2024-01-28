from src.refactor_tests import create_playlist_from_files as cp, create_new_files as cnf, sort_tests_to_files as sttf
import src.application_properties as ap
import src.gen_files.enums
from src.gen_files import paths as p
from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf


def main_script():
    pf.print_step_separator("Source Compare")
    print("Enter 2 different lists of test, to see discrepancies between the 2 lists.")
    pf.print_bold("\nSource 1:")
    test_names1 = ih.get_test_paths_from_input(get_only_test_names=True)
    pf.print_bold("\nSource 2:")
    test_names2 = ih.get_test_paths_from_input(get_only_test_names=True)
    differences_list = get_dif_str_from_lsts(test_names1, test_names2)
    pf.print_note("\n\nTests found only in Source 1 (" + str(len(differences_list[0])) + "):")
    pf.print_list_by_row(differences_list[0])
    pf.print_note("\n\nTests found only in Source 2 (" + str(len(differences_list[1])) + "):")
    pf.print_list_by_row(differences_list[1])
    pf.print_note("\n\nTests found in both Sources (" + str(len(differences_list[2])) + "):")
    pf.print_list_by_row(differences_list[2])
    pf.print_note("\n Total tests analyzed: " + str(sum(len(sublist) for sublist in differences_list)) + ". "
                  + "Only in Source 1: " + str(len(differences_list[0])) + " . Only in Source 2: " + str(len(differences_list[1])))


def get_dif_str_from_lsts(test_names1, test_names2):
    set1 = set(test_names1)
    set2 = set(test_names2)

    # items that exist only in test_names1
    only_in_test_names1 = set1 - set2
    res1 = [item for item in test_names1 if item in only_in_test_names1]
    # items that exist only in test_names2
    only_in_test_names2 = set2 - set1
    res2 = [item for item in test_names2 if item in only_in_test_names2]
    # items that exist in both
    res3 = list(set1.intersection(set2))

    return [res1, res2, res3]





if __name__ == '__main__':
    main_script()
