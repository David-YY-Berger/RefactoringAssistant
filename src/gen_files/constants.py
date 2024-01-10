from enum import Enum

empty_csv = "-"
not_found = "not found"
java_ext = ".java"


class Servers(Enum):
    QAC01 = 0
    SQA_EU01 = 1
    SQA_NA01 = 2
    COULD_NOT_FIND_SERVER = 3


class Cmds(Enum):
    BY_DIR = 0
    BY_LIST = 1