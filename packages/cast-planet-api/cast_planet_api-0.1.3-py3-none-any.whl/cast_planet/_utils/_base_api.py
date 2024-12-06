from logging import Logger
from typing import Union, Any, Dict

from pydantic import ValidationError
from requests import Session, RequestException

from cast_planet._utils._session_factory import create_session
from cast_planet._utils._functions import setup_logger


class BaseApi:
    _base_url: str
    _session: Session
    _logger: Logger

    def __init__(self, api_key: str, base_url: str, log_filename: Union[str, None] = None, log_level: int = None):
        """
        Initializes the BaseApi class with the provided API key, base URL, and optional log file name.

        This class serves as the base class for interacting with the API, providing methods for GET and POST requests,
        as well as centralized error handling and logging.

        :param api_key: The API key used to authenticate requests to the API.
        :param base_url: The base URL of the API (must include the domain and optionally a path).
        :param log_filename: If provided, logs will be written to this file. If None, logs will be directed to the console.
        """
        self._base_url = base_url.rstrip('/')  # Strip trailing slashes for consistency
        self._logger = setup_logger(log_filename, log_level)  # Set up logging with optional file output
        self._session = create_session(api_key, self._logger)  # Initialize session with provided API key and logger

    def __handle_response__(self, response) -> Dict[str, Any]:
        """
        Handles HTTP response and raises appropriate exceptions if the response status is not OK.

        This method checks if the response status code is OK (i.e., 2xx), processes the JSON content,
        and returns the result. If any issues are encountered (e.g., HTTP error or invalid JSON response),
        an error is logged, and an exception is raised.

        :param response: The HTTP response object to be processed.
        :return: The JSON-decoded response data if the status code is OK.
        :raises RequestException: If the response status code indicates an error or if the request fails.
        :raises ValidationError: If the response cannot be parsed as JSON or does not match the expected structure.
        """
        try:
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except RequestException as e:
            self._logger.error(f"Request failed: {e}")
            raise  # Propagate the exception
        except ValidationError as e:
            self._logger.error(f"Invalid response format: {e}")
            raise  # Propagate the exception

    def __generate_endpoint__(self, endpoint):
        return endpoint if endpoint.startswith('http') else f"{self._base_url}{endpoint}"

    def _get(self, endpoint: str, params: dict = None) -> Dict[str, Any]:
        """
        Helper method for making GET requests to the API.

        This method is used to perform a GET request to the API with optional query parameters. It handles
        response errors and logs the request and response details.

        :param endpoint: The endpoint to append to the base URL for the GET request.
        :param params: Optional dictionary of query parameters to include in the GET request.
        :return: The JSON-decoded response data.
        :raises Exception: If the GET request fails or returns an error.
        """
        try:
            response = self._session.get(self.__generate_endpoint__(endpoint), params=params)
            return self.__handle_response__(response)
        except Exception as e:
            self._logger.error(f"Error with GET request to {endpoint}: {e}")
            raise  # Propagate the exception

    def _post(self, endpoint: str, data: dict = None, params: dict = None) -> Dict[str, Any]:
        """
        Helper method for making POST requests to the API.

        This method is used to perform a POST request to the API with a JSON payload. It handles response errors
        and logs the request and response details.

        :param endpoint: The endpoint to append to the base URL for the POST request.
        :param data: Optional dictionary of data to send as the JSON payload in the POST request.
        :return: The JSON-decoded response data.
        :raises Exception: If the POST request fails or returns an error.
        """
        try:

            response = self._session.post(self.__generate_endpoint__(endpoint), json=data, params=params)
            return self.__handle_response__(response)
        except Exception as e:
            self._logger.error(f"Error with POST request to {endpoint}: {e}")
            raise  # Propagate the exception
