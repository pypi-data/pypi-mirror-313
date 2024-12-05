from enum import Enum


class TestStatus(str, Enum):
    success = "success"
    warning = "warning"
    fail = "fail"
