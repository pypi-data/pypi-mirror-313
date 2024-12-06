from datetime import datetime, timezone
from typing import Any, Optional
from foxsenseinnovations.vigil.vigil_types.exception_log_types import ExceptionExtraAttributes
import traceback
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.api_service import ApiService
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
class ErrorMonitoring:
    """
    ErrorMonitoring captures and logs exceptions, sending relevant data to Vigil for monitoring and analysis.
    Attributes:
        None
    """
    def capture_exception(
        self,
        exception: Any,
        extra_attributes: Optional[ExceptionExtraAttributes] = None,
        isUnhandled: Optional[bool] = False
    ) -> None:
        """
        Captures an exception and sends data to Vigil for monitoring.
        Args:
            exception (Any): The exception object.
            extra_attributes (Optional[ExceptionExtraAttributes]): Extra attributes related to the exception
            (default None).
        Returns:
            None
        """
        frames = traceback.extract_tb(exception.__traceback__)
        frames_info = [
            {
                'beforeParse': repr(frame),
                'fileName': frame.filename,
                'functionName': frame.name,
                'functionShortName': frame.name,
                'fileFullPath': frame.filename,
                'lineNo': frame.lineno
            }
            for frame in frames
        ]
        error_data = {
            "clientVersion": extra_attributes.get('client_version') if extra_attributes and extra_attributes.get('client_version') is not None else Vigil.version,
            "error": {
                "name": exception.__class__.__name__,
                "message": str(exception),
                "stack": traceback.format_exc() if isUnhandled is False else ''.join(traceback.format_exception(exception.__class__.__name__, exception, exception.__traceback__)),
                "stackFrames": frames_info
            },
            "tags": extra_attributes.get('tags') if extra_attributes and extra_attributes.get('tags') is not None else None,
            "context": extra_attributes.get('context') if extra_attributes and extra_attributes.get('context') is not None else None,
            "reportedAt": datetime.now(timezone.utc).isoformat(),
        }

        try:
            ApiService.make_api_call(
                Vigil.instance_url,
                RouteConstants.ERROR_MONITORING,
                error_data,
                Vigil.api_key
            )
            logging.info('[Vigil] Exception record added successfully')
        except Exception as e:
            logging.error(f"[Vigil] Error while creating exception log: {e}")
            

ErrorManager = ErrorMonitoring()
