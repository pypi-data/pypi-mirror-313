from typing import Optional

class VigilOptions:
    """
    Represents options for configuring Vigil monitoring.
    Attributes:
        api_key (str): API key used for authentication with Vigil.
        client_version (Optional[str]): Version of the client application using Vigil.
        instance_url (Optional[str]): URL of the Vigil instance to connect to.
    """
    def __init__(self, api_key: str, client_version: Optional[str] = None, instance_url: Optional[str] = None) -> None:
        self.api_key = api_key
        self.client_version = client_version
        self.instance_url = instance_url