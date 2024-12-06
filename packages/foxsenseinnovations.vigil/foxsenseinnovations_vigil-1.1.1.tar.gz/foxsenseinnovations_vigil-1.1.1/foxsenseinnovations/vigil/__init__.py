from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.error_manager import ErrorManager
from foxsenseinnovations.vigil.job_manager import JobManager
from foxsenseinnovations.vigil.vigil_types.vigil_options_types import *
from foxsenseinnovations.vigil.vigil_types.job_monitoring_types import *
from foxsenseinnovations.vigil.vigil_types.exception_log_types import *
import sys
import traceback
import logging

__all__ = ['Vigil', 'ErrorManager', 'JobManager']

def log_except_hook(exc_type, exc_value, exc_traceback):
    text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.error("Unhandled exception: %s", text)
    ErrorManager.capture_exception(exc_value, {'tags': ['Server crash']}, isUnhandled=True)
sys.excepthook = log_except_hook