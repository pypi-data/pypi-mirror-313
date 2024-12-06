import os

class SDKConnection:
    
    client = None

    def __init__(self, api_url: str = os.getenv("ARGILLA_API_URL"), api_key: str = os.getenv("ARGILLA_API_KEY"), **kwargs):
        self._initialize_connection(api_url, api_key, **kwargs)

    def _initialize_connection(self, api_url: str, api_key: str, **kwargs):
        """
        Initialize the connection to the Argilla API.
        Parameters:
            api_url (str): The URL of the Argilla API.
            api_key (str): The API key for the Argilla API.
        """
        if not api_url:
            raise ValueError("ARGILLA_API_URL is not set in the environment variables")
        if not api_key:
            raise ValueError("ARGILLA_API_KEY is not set in the environment variables")

        import argilla as rg
        
        self.client = rg.Argilla(
            api_url=api_url,
            api_key=api_key,
            **kwargs
        )

    