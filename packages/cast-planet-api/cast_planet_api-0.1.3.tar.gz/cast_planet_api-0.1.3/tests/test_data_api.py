import unittest
from typing import Any, Dict
from unittest import mock

from cast_planet.data import DataAPI, ItemType

# mocks
from cast_planet._utils._session_factory import Session

BASE_URL = 'https://unittest.com'
BASE_URL_SLASH = f'{BASE_URL}/'


def generate_item_types() -> Dict[str, Any]:
    items_types = [{
        'id': str(i),
        'display_description': f'Item {i} description.',
        'display_name': f'Item Type {i}',
        'supported_asset_types': [f'asset_{x}' for x in range(3)]
    } for i in range(5)]
    return {'item_types': items_types}


def mock_item_types_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.url = args[1]

        def json(self):
            return self.json_data

        def raise_for_status(self):
            # We are assuming that the other
            return True

    if args[1] == f'{BASE_URL}/item-types':
        return MockResponse(generate_item_types(), 200)

    return MockResponse(None, 404)


class TestGetItemTypes(unittest.TestCase):

    @mock.patch.object(Session, "get", new_callable=lambda: mock_item_types_get)
    def test_get_types_should_return_list_of_item_types(self, not_needed_but_required):
        sut = DataAPI(api_key='MockApiKey', base_url=BASE_URL)

        result = sut.item_types()

        self.assertEqual(5, len(result))
        self.assertEqual(type(result[0]), ItemType)
