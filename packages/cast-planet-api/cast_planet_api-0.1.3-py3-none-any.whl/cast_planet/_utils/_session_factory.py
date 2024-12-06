from logging import Logger
from requests import Session, Response
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from cast_planet.exceptions import (NoApiKeyException, BadRequest400Error, PermissionDenied401Error,
                                    NotFound404Error, CouldNotComplete409Error, InternalServerErrorException)


def handle_planet_responses(func, logger):
    """
    Wraps an HTTP request function to handle and log responses, raising exceptions for HTTP statuses that do not
    require retries.

    This decorator function logs the HTTP response status code and URL for debugging purposes.
    If the response status code indicates a client or server error (like 400, 401, 404, 409, or 500),
    it logs the error message and raises the corresponding exception.

    :param func: The original HTTP request function (e.g., `session.get` or `session.post`) that will be wrapped.
    :param logger: Logger instance to log HTTP response details and errors.

    :return: The original HTTP response if the status code is successful (i.e., not in the error ranges).
    :raises BadRequest400Error: If the HTTP status code is 400 (Bad Request).
    :raises PermissionDenied401Error: If the HTTP status code is 401 or 403 (Permission Denied).
    :raises NotFound404Error: If the HTTP status code is 404 (Not Found).
    :raises CouldNotComplete409Error: If the HTTP status code is 409 (Conflict).
    :raises InternalServerErrorException: If the HTTP status code is 500 (Internal Server Error).
    """

    def with_response_handling(*args, **kwargs):
        r: Response = func(*args, **kwargs)

        # Logging for all responses for better debugging
        logger.debug(f"HTTP {r.status_code} - {r.url}")

        if r.status_code == 400:
            logger.error(f"Bad request: {r.text}")
            raise BadRequest400Error()
        if r.status_code == 401 or r.status_code == 403:
            logger.error(f"Permission denied: {r.text}")
            raise PermissionDenied401Error()
        if r.status_code == 404:
            logger.error(f"Not found: {r.text}")
            raise NotFound404Error()
        if r.status_code == 409:
            logger.error(f"Conflict: {r.text}")
            raise CouldNotComplete409Error()
        if r.status_code == 500:
            logger.error(f"Internal server error: {r.text}")
            raise InternalServerErrorException()

        return r

    return with_response_handling


def create_session(api_key: str, logger: Logger, total: int = 3, backoff_factor: int = 3, retry_statuses=None):
    """
    Creates a configured requests Session object to interact with the Planet REST API, with automatic retries and logging.

    This function sets up a `requests.Session` for making API calls, with support for retrying requests
    when certain status codes (e.g., 429, 500) are returned. The session also includes a custom response
    handler that logs errors based on HTTP status codes and raises exceptions when necessary.

    :param api_key: A valid API key required to authenticate API requests to the Planet API.
    :param logger: Logger instance used to log details about requests, responses, and errors.
    :param total: Total number of retries for a failed API call. Default is 3 retries.
                  This parameter controls how many times a request should be retried in case of failure.
    :param backoff_factor: A factor to calculate the delay between retries. Default is 3.
                           A higher value results in longer delays between retries.
    :param retry_statuses: A list of HTTP status codes that should trigger a retry.
                            Defaults to [429, 500, 502, 503, 504].

    :return: A `requests.Session` object configured with retries, logging, and response handling.
    :raises NoApiKeyException: If the API key is missing or invalid.
    """
    if api_key is None:
        logger.error("API key is missing")
        raise NoApiKeyException()

    if retry_statuses is None:
        retry_statuses = (429, 500, 502, 503, 504)

    retry = Retry(
        total=total,
        backoff_factor=backoff_factor,
        status_forcelist=retry_statuses,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session = Session()
    session.auth = (api_key, '')
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    # Apply the response handling decorator with the logger injected
    session.get = handle_planet_responses(session.get, logger)
    session.post = handle_planet_responses(session.post, logger)

    return session
