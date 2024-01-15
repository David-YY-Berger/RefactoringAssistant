from enum import Enum, auto


class Servers(Enum):
    QAC01 = 0
    SQA_EU01 = 1
    SQA_NA01 = 2
    COULD_NOT_FIND_SERVER = 3
    IGNORE = 4


class OptionsInputTests(Enum):
    BY_DIRECTORY_PATH = 1
    BY_A_LIST_OF_TEST_NAMES = 2
    BY_PATH_TO_EXCEL_FILE = 3


class OptionsYesNo(Enum):
    YES = 1
    NO = 2
