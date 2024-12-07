import logging
import unittest
from enum import Enum


# ---------------------------------------------------------

class CaseStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"

    def get_log_level(self) -> int:
        status_to_logging = {
            CaseStatus.SUCCESS: logging.INFO,
            CaseStatus.ERROR: logging.CRITICAL,
            CaseStatus.FAIL: logging.ERROR,
            CaseStatus.SKIPPED: logging.INFO
        }
        return status_to_logging[self]


class CaseReport:
    def __init__(self, name : str, status : CaseStatus, runtime : float):
        self.runtime_sec : float = runtime
        self.name : str = name
        self.status : CaseStatus = status


class CustomTestCase(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.is_manual_mode : bool = False

    def set_manual(self):
        self.is_manual_mode = True

    def get_is_manual(self):
        return self.is_manual_mode

    # ---------------------------------------------------------

    def make_report(self, status : CaseStatus, runtime : float) -> CaseReport:
        return CaseReport(name=self.get_name(), status=status, runtime=runtime)

    def get_name(self) -> str:
        full_test_name = self.id()
        parts = full_test_name.split('.')
        last_parts = parts[-2:]
        test_name = '.'.join(last_parts)
        return test_name

