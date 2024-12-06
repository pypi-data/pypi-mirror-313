from requests import RequestException


class PlanetAPIException(RequestException):
    """ Base exception for all custom Planet API exceptions """
    pass


class PermissionDenied401Error(PlanetAPIException):
    """
    API responded with 401: Permission denied status. Check your API key.
    """
    def __init__(self, message="API responded with 401: Permission denied. Check your API key.", *args):
        super().__init__(message, *args)


class CouldNotComplete409Error(PlanetAPIException):
    """
    API responded with '409: Could not complete' the requested task. Check the status of the item/asset/order.
    """
    def __init__(self, message="API responded with 409: Could not complete the task. Check the status of the item.", *args):
        super().__init__(message, *args)


class BadRequest400Error(PlanetAPIException):
    """ API responded with 400: Bad Request status. """
    def __init__(self, message="API responded with 400: Bad Request. Check the request format or parameters.", *args):
        super().__init__(message, *args)


class NoApiKeyException(Exception):
    """ No Planet API key provided. """
    def __init__(self, message="No Planet API key provided. Please provide a valid API key.", *args):
        super().__init__(message, *args)


class NotFound404Error(PlanetAPIException):
    """ API responded with 404: Not Found. """
    def __init__(self, message="API responded with 404: Resource not found.", *args):
        super().__init__(message, *args)


class AssetNotFoundException(Exception):
    """ Asset ID not found in list of available assets """
    def __str__(self):
        return f'{type(self)}: Asset ID not found in list of available assets'


class InternalServerErrorException(PlanetAPIException):
    """ API responded with 500: Internal Server Error status. """
    def __init__(self, message="API responded with 500: Internal server error. Try again later.", *args):
        super().__init__(message, *args)
