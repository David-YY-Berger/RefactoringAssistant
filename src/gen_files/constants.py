from enum import Enum

empty_char = "-"
not_found = "not found"
not_find_testng = "not find testng"
java_ext = ".java"
line = ('----------------------------------------------------------------------------------------------------------'
        '------------------------------------------------------------------------------')


class Servers(Enum):
    QAC01 = 0
    SQA_EU01 = 1
    SQA_NA01 = 2
    COULD_NOT_FIND_SERVER = 3
    IGNORE = 4


class OptionsInputTests(Enum):
    BY_DIRECTORY_PATH = 0
    BY_A_LIST_OF_TEST_NAMES = 1