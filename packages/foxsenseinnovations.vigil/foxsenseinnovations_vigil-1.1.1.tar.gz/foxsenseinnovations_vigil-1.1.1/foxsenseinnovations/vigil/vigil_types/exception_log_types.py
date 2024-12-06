from typing import Optional, List, Dict
class ExceptionExtraAttributes:
    """
    Represents additional attributes for an exception.
    Attributes:
        tags: Optional list of tags associated with the exception.
        context: Optional dictionary containing additional context for the exception.
        client_version: Optional version of the client where the exception occurred.
    """
    def __init__(
        self,
        tags: Optional[List[str]] = None,
        context: Optional[Dict] = None,
        client_version: Optional[str] = None,
    ):
        self.tags = tags
        self.context = context
        self.client_version = client_version