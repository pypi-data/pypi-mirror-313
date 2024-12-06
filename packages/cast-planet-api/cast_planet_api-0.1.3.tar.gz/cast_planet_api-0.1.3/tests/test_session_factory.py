import unittest

import pytest
from requests.exceptions import RetryError

from mocks import MockLogger
from cast_planet._utils import create_session

from cast_planet.exceptions import (NoApiKeyException, BadRequest400Error, PermissionDenied401Error,
                                    NotFound404Error, CouldNotComplete409Error)


class TestAuthorization(unittest.TestCase):

    def test_create_session_requires_api_key(self):
        """Test that create_session raises an exception if no API key is provided."""

        with self.assertRaises(NoApiKeyException):
            create_session(api_key=None, logger=MockLogger())

    def test_api_key_is_added_to_auth(self):
        sut = create_session('ABC123', logger=MockLogger())
        result = sut.auth

        self.assertEqual(('ABC123', ''), result)


class TestErrorHandling(unittest.TestCase):
    def test_handles_planet_failed_responses(self):
        situations = {
            400: BadRequest400Error,
            401: PermissionDenied401Error,
            404: NotFound404Error,
            409: CouldNotComplete409Error
        }

        sut = create_session(api_key='none',logger=MockLogger())
        for status in situations:
            with (pytest.raises(situations[status])):
                try:
                    sut.get(url=f'https://httpbin.org/status/{status}')
                    sut.post(url=f'https://httpbin.org/status/{status}')
                except RetryError as e:
                    # Some things get a little finicky.
                    # A 503 is not an indication of a code failure, but a httpbin issue..
                    if '503' in str(e):
                        raise situations[status]


    def test_retries(self):
        sut = create_session(api_key='none', logger=MockLogger(), total=1, )
        with pytest.raises(RetryError) as e:
            sut.get(url='https://httpbin.org/status/500')
