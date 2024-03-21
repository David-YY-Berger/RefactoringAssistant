from enum import Enum, auto


def get_name_from_value_enum(val, enum_class):
    enum_dict = {item.value: item.name for item in enum_class}
    return enum_dict.get(val, 'could not find enum with value ' + str(val))


def readable(str):
    return str.capitalize().replace('_', ' ')


class Servers(Enum):
    QAC01 = 0
    SQA_EU01 = auto()
    SQA_NA01 = auto()
    SQA02_NA03 = auto()
    COULD_NOT_FIND_SERVER = auto()
    IGNORE = auto()
    SQA_EU03 = auto()
    SQA_NA02 = auto()
    SQA_EU04 = auto()
    SQA_EU02 = auto()


class OptionsInputTests(Enum):
    BY_DIRECTORY_PATH = auto()
    BY_A_LIST_OF_TEST_NAMES = auto()
    BY_PATH_TO_EXCEL_FILE = auto()
    BY_PATH_TO_CSV_FILE = auto()
    # GET_ALL_TESTS_IN_TESTNG_FILES = auto()


class OptionsYesNo(Enum):
    YES = auto()
    NO = auto()


class MainOptions(Enum):
    REFACTOR_TESTS = auto()
    TEST_LIST_COMPARE = auto()
    DISCREPANCY_TRACKER = auto()
    # LOGIN_AS_ADMIN = auto()
    SETUP = auto()
    EXIT = auto()


class DiscrepancyTrackerOptions(Enum):
    FIND_AND_PROCCESS_DISCREPANCIES = auto()
    COMPARE_DISCREPANCIES = auto()


class DefaultKeywordsChoiceOptions(Enum):
    KEYWORDS1_ONLY = auto()
    KEYWORDS2_ONLY = auto()
    BOTH = auto()
    PROMPT_USER = auto()


class PromptUserKeywordOptions(Enum):
    KEYWORDS1_ONLY = auto()
    KEYWORDS2_ONLY = auto()
    BOTH = auto()


class CustomOrDefaultConfig(Enum):
    DEFAULT_CONFIG = auto()
    CUSTOM_CONFIG = auto()
    OVERWRITE_MY_CUSTOM_CONFIG_WITH_DEFULT = auto()