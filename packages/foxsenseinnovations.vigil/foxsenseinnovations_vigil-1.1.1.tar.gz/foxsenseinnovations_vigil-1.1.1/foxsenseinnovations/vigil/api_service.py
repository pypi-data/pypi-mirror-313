from typing import Any, Dict
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
class ApiService:
    """
    ApiService is a utility class for making HTTP POST requests to external APIs. Its static method,
    make_api_call, constructs the API endpoint URL and sends a POST request with provided data and headers,
    including an API key for authorization. It abstracts away HTTP request complexity, leveraging the requests
    library, and offers a centralized interface for API interaction within applications.
    """
    @staticmethod
    def make_api_call(
        base_url: str,
        api_url: str,
        data: Dict[str, Any],
        header: str
    ) -> requests.Response:
        try:
            actual_url = base_url + api_url
            headers = {'x-api-key': header}
            response = requests.post(
                actual_url,
                json = data,
                headers=headers,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            error_response = response.json()
            error_message = error_response.get('error', {}).get('message', response.text)
            logging.error(f"Error Message: {error_message}")
            raise e
