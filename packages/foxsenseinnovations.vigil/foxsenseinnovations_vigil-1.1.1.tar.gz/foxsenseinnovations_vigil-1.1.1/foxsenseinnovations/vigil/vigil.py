from foxsenseinnovations.vigil.vigil_types.vigil_options_types import VigilOptions

class Vigil:
    """
    Vigil class represents the configuration settings for Vigil.
    Attributes:
        api_key (str): The API key used for authentication.
        version (str): The client version.
        instance_url (str): The URL of the Vigil instance.
    """
    api_key: str = ""
    version: str = ""
    instance_url: str = ""

    @classmethod
    def initialize(cls, options: VigilOptions) -> None:
        """
        Initializes the Vigil class with the provided options.
        Args:
            options (VigilOptions): An instance of VigilOptions containing the configuration settings.
        Returns:
            None
        """
        cls.api_key = options.api_key
        cls.version = options.client_version if options.client_version is not None else ""
        cls.instance_url = options.instance_url if options.instance_url is not None else 'https://api.vigilnow.com'