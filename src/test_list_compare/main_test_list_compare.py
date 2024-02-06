from src.gen_files.ConsoleHelpers import input_helper as ih, print_functions as pf
from src.gen_files import gen_scripts as gs, stats_for_metrics as sfm
from src import application_properties as ap
from src.Classes.test_class import Test
from src.gen_files import enums as enums


def main_script():
    pf.print_step_separator("Source Compare")
    print("Enter 2 different lists of test, to see discrepancies between the 2 lists.")

    pf.print_bold("\nSource 1:")
    [test_obj_list1, src_type1] = ih.get_test_objs_from_input(get_source_type=True)

    pf.print_bold("\nSource 2:")
    [test_obj_list2, src_type2] = ih.get_test_objs_from_input(get_source_type=True)

    print_found_in_both = False
    cmd = ih.get_input_enum_options("Print the tests found in both sources?", list(enums.OptionsYesNo))
    if cmd == enums.OptionsYesNo.YES.value:
        print_found_in_both = True

    differences_list = get_dif_array_from_test_objs(test_obj_list1, test_obj_list2)
    tests_only_in_src1 = get_nice_string_list_test_name_section(differences_list[0])
    tests_only_in_src2 = get_nice_string_list_test_name_section(differences_list[1])

    pf.print_note("\n\n" + str(len(tests_only_in_src1)) + " Tests found only in Source 1 (" + src_type1 +")")
    if tests_only_in_src1:
        pf.print_list_by_row(tests_only_in_src1)

    pf.print_note("\n\n" + str(len(tests_only_in_src2)) + " Tests found only in Source 2 (" + src_type2 + ")")
    if tests_only_in_src2:
        pf.print_list_by_row(tests_only_in_src2)

    if print_found_in_both:
        pf.print_note("\n\nTests found in both Sources (" + str(len(differences_list[2])) + " tests):")
        pf.print_list_by_row(differences_list[2])

    pf.print_note("\nTotal tests analyzed: " + str(sum(len(sublist) for sublist in differences_list)) + ".\n"
                  + "Only in Source 1 (" + src_type1 +"): " + str(len(tests_only_in_src1)) + "\n" +
                  "Only in Source 2 (" + src_type2 +"): " + str(len(tests_only_in_src2)) + "\n" +
                  "In Both: " + str(len(differences_list[2])))

    sfm.append_to_stats(version=ap.version, user_name=gs.get_cur_user_name(), date=gs.get_date(), time=gs.get_time(),
                         product=sfm.product_names.Test_List_Compare.name, is_success=True, missing_files_found=len(tests_only_in_src1) + len(tests_only_in_src2))


def get_dif_array_from_test_objs(test_obj_list1, test_obj_list2):
    set1 = set([test.test_name for test in test_obj_list1])
    set2 = set([test.test_name for test in test_obj_list2])

    # items that exist only in test_obj_list2
    only_in_test_names1 = set1 - set2
    res1 = [item for item in test_obj_list1 if item.test_name in only_in_test_names1]
    # items that exist only in test_obj_list2
    only_in_test_names2 = set2 - set1
    res2 = [item for item in test_obj_list2 if item.test_name in only_in_test_names2]
    # items that exist in both - only include names!!
    res3 = list(set1.intersection(set2))

    return [res1, res2, res3]


def get_nice_string_list_test_name_section(test_obj_list):
    if len(test_obj_list) == 0:
        return ''
    test_obj_list = remove_test_obj_duplicates_name_section(test_obj_list)
    test_obj_list = Test.order_by_section(test_obj_list)
    dif_max_length = len(max([test.test_name for test in test_obj_list], key=len))
    return [gs.space_nicely(test.test_name, dif_max_length, " | " + test.test_section) for test in test_obj_list]


def remove_test_obj_duplicates_name_section(test_obj_list):
    seen = set()
    unique_tests = []
    for test in test_obj_list:
        if not any(Test.same_test_name_and_section(test, seen_test) for seen_test in seen):
            unique_tests.append(test)
            seen.add(test)
    return unique_tests



if __name__ == '__main__':
    main_script()
