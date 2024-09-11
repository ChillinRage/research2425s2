from enum import Enum

class Category(Enum):
    INIT = 0
    PASS = 1
    WRONG = 2
    COMPILE_ERROR = 3
    MISSING_FUNCTION = 4
    RUN_ERROR = 5
    TLE = 6
    BLANK = 7
    LENGTH = 8
