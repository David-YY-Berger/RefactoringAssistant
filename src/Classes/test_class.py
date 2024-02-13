from src.gen_files import constants as cons


class Test:
    # Static fields
    TEST_NAME_FIELD = 'test_name'
    TEST_PATH_FIELD = 'test_path'
    TEST_SECTION_FIELD = 'test_section'
    TEST_RESULT_FIELD = 'test_result'
    TESTNG_FILE_NAME_FIELD = 'testng_file_name'
    TEST_PATH_NG_FIELD = 'test_path_ng'
    DISCREPANCY_FIELD = 'discrepancy'

    def __init__(self, test_name, test_path=cons.empty_char, test_section=cons.empty_char, test_result=cons.empty_char,
                 testng_file_name=cons.empty_char, test_path_ng=cons.empty_char, discrepancy = cons.empty_char):
        self.test_name = test_name
        self.test_path = test_path
        self.test_section = test_section
        self.test_result = test_result
        self.testng_file_name = testng_file_name
        self.test_path_ng = test_path_ng
        self.discrepancy = discrepancy

    @staticmethod
    def same_test_name_and_section(test_obj1, test_obj2):
        return test_obj1.test_name == test_obj2.test_name and test_obj1.test_section == test_obj2.test_section

    @staticmethod
    def order_by_section(test_obj_list):
        return sorted(test_obj_list, key=lambda test: (test.test_section, test.test_name))


class TestAndResult:
    def __init__(self, test_name, test_result):
        self.test_name = test_name
        self.test_result = test_result


