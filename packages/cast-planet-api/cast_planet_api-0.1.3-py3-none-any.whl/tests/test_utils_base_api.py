import unittest
from unittest.mock import patch, MagicMock

from requests import HTTPError, Response

from cast_planet._utils import BaseApi


class TestBaseApiSetup(unittest.TestCase):

    def test_base_url_handles_slash(self):
        sut = BaseApi(api_key='MockApiKey', base_url='http://a.url.with/ending-slash/')
        self.assertEqual('http://a.url.with/ending-slash', sut._base_url)


class TestBaseFailures(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.base_url = "https://api.test.com"
        self.log_filename = None
        self.api = BaseApi(self.api_key, self.base_url, self.log_filename)

    @patch("cast_planet._utils._session_factory.create_session")
    def test_get_raises_404_exception(self, mock_create_session):
        # Mock session and response
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error: Not Found")
        mock_session.get.return_value = mock_response
        mock_create_session.return_value = mock_session

        self.api._session = mock_session

        with self.assertRaises(HTTPError) as context:
            self.api._get("/non-existent-endpoint")

        self.assertIn("404 Client Error: Not Found", str(context.exception))
        mock_session.get.assert_called_once_with(f"{self.base_url}/non-existent-endpoint", params=None)

    @patch("cast_planet._utils._session_factory.create_session")
    def test_post_raises_404_exception(self, mock_create_session):
        # Mock session and response
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error: Not Found")
        mock_session.post.return_value = mock_response
        mock_create_session.return_value = mock_session

        self.api._session = mock_session

        with self.assertRaises(HTTPError) as context:
            self.api._post("/non-existent-endpoint", data={"key": "value"})

        self.assertIn("404 Client Error: Not Found", str(context.exception))
        mock_session.post.assert_called_once_with(
            f"{self.base_url}/non-existent-endpoint", json={"key": "value"}, params=None
        )


class TestHandleResponse(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.base_url = "https://api.test.com"
        self.log_filename = None
        self.api = BaseApi(self.api_key, self.base_url, self.log_filename)

    def mock_response(self, status_code=200, json_data=None, raise_for_status=None):
        """
        Helper method to create a mocked response object.
        """
        mock_resp = MagicMock(spec=Response)
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        return mock_resp

    def test_handle_response_success(self):
        """
        Test that _handle_response successfully returns the response when status is 2xx.
        """
        mock_resp = self.mock_response(status_code=200, json_data={"key": "value"})

        result = self.api.__handle_response__(mock_resp)
        self.assertEqual(result, mock_resp.json())

    def test_handle_response_http_error(self):
        """
        Test that _handle_response raises HTTPError on 4xx/5xx responses.
        """
        mock_resp = self.mock_response(
            status_code=404,
            raise_for_status=HTTPError("404 Client Error: Not Found")
        )

        with self.assertRaises(HTTPError) as context:
            self.api.__handle_response__(mock_resp)

        self.assertIn("404 Client Error: Not Found", str(context.exception))

    def test_handle_response_invalid_json(self):
        """
        Test that _handle_response raises a generic exception when JSON decoding fails.
        """
        mock_resp = self.mock_response(status_code=200)
        mock_resp.json.side_effect = ValueError("Invalid JSON")

        # The code does not specifically handle JSON decode errors, so this is hypothetical.
        # You could extend `_handle_response` to catch JSON decode errors and raise an exception if needed.
        with self.assertRaises(ValueError) as context:
            self.api.__handle_response__(mock_resp)

        self.assertIn("Invalid JSON", str(context.exception))

    def test_handle_response_no_content(self):
        """
        Test that _handle_response works with a response with no content (e.g., 204 No Content).
        """
        mock_resp = self.mock_response(status_code=204, json_data=None)

        result = self.api.__handle_response__(mock_resp)
        self.assertEqual(result, mock_resp.json())


class TestGenerateEndpoint(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.base_url = "https://api.test.com"
        self.log_filename = None
        self.api = BaseApi(self.api_key, self.base_url, self.log_filename)

    def test_get_url_with_base_attached(self):
        """
        Test that a relative endpoint returns with the baseurl attached
        """


        result = self.api.__generate_endpoint__('/relative')
        self.assertEqual(result, "https://api.test.com/relative")

    def test_get_a_full_url(self):
        """
        Test that a full endpoint doesn't have the base added to it.
        The self and next links that are returned with objects return with the full url of the link
        no base url is needed.
        """
        full_url = "https://api.test.com/full"
        result = self.api.__generate_endpoint__(full_url)
        self.assertEqual(result, full_url)
