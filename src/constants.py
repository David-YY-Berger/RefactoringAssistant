from enum import Enum

empty_csv = "-"
not_found = "not found"


class Servers(Enum):
    QAC01 = 0
    SQA_EU01 = 1
    SQA_NA01 = 2
    NOT_FIND_SERVER = 3
