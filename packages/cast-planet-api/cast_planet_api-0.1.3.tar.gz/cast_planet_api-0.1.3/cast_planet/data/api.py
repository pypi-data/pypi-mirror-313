import os
from io import BytesIO
from typing import List, Dict, Any, Union, Optional
from uuid import UUID

from IPython import display
from PIL import Image

from cast_planet._utils import BaseApi, download_file
from cast_planet.exceptions import AssetNotFoundException
from cast_planet.data.filters.permission import __wrap_filter_with_permissions__

from cast_planet.data.filters.base import BaseFilter
from cast_planet.data.models import ItemAsset, QuickSearchItem, ItemType, QuerySort, QuickSearchResponse, ItemAssetStatus


def __feature_dicts_to_response_feature__(features: List[Dict[str, Any]]) -> List[QuickSearchItem]:
    return [QuickSearchItem(**f) for f in features]


def __item_type_request__(item_types: List[Union[str, ItemType]]):
    request_item_types: List[str] = list()
    for i in item_types:
        if isinstance(i, ItemType):
            request_item_types.append(i.id)
        elif isinstance(i, str):
            request_item_types.append(i)
        else:
            raise ValueError('str or ItemType required.')
    return request_item_types


class DataAPI(BaseApi):
    """
    Wrapper class for interacting with the Planet Data API.
    Provides methods for searching, retrieving, and managing items,
    item assets, and item types.


    See the Planet Data API documentation for more details:
    https://developers.planet.com/docs/apis/data/

    Args:
        api_key: The planet API key for your subscription.
        base_url: ase_url: The base URL of the Planet Data API (default: 'https://api.planet.com/data/v1')
        logging_filepath: If supplied, class will log to file.
        log_level: If supplied, sets the log level for the class. Default logging level is logging.ERROR.
    """
    _page_size = 20

    def __init__(self, api_key: str, base_url: str = "https://api.planet.com/data/v1",
                 logging_filepath: Optional[str] = None, log_level: Optional[int] = None):
        """
        Initializes the DataAPI client with the provided API key and base URL.
        """
        super().__init__(api_key, base_url, logging_filepath, log_level)

    def __gather_features_from_response__(self, response_data: Dict[str, Any]) -> List[QuickSearchItem]:
        """
        Helper method that processes a paginated response from the quick search API.

        It retrieves all features by iterating through pages until no more results
        are available.

        :param response: The HTTP response object from a quick search request.
        :return: A list of QuickSearchItem objects representing the features from the response.
        """
        features = gathered_features = __feature_dicts_to_response_feature__(response_data['features'])

        while len(features) == self._page_size:
            next_url = response_data['_links']['_next']
            response_data = self._get(endpoint=next_url)
            features = __feature_dicts_to_response_feature__(response_data['features'])
            gathered_features.extend(features)
        return gathered_features

    def item_types(self) -> List[ItemType]:
        """
        Retrieves all available item types from the Planet Data API.

        This method calls the `/item-types` endpoint to list the supported item types.

        :return: A list of ItemType objects representing all available item types.
        """
        response_data = self._get(f'/item-types')
        return [ItemType(**x) for x in response_data['item_types']]

    def get_item(self, item_type: Union[ItemType, str], item_id: Union[UUID,str]):
        if isinstance(item_type, ItemType):
            item_type = item_type.id
        response = self._get(f'/item-types/{item_type}/items/{item_id}')
        return QuickSearchItem(**response)

    def quick_search(self, item_types: List[Union[ItemType, str]], search_filter: BaseFilter,
                     asset_types: List[str] = None, name: str = None,
                     sort: QuerySort = None, permissions: bool = True) -> QuickSearchResponse:
        """
        Searches for items that match the provided filter criteria. Optionally, results
        can be filtered by asset types, name, and sorting options. Permissions can also be
        applied to limit the search to items with download permissions.

        The search criteria are combined into a request body, which is then sent to the
        `/quick-search` endpoint of the Planet Data API.

        :param item_types: Required. A list of item types to include in the search.
                            Can be a mix of ItemType objects and strings representing item types.
        :param search_filter: Required. A filter to limit the search results.
        :param asset_types: Optional. A list of asset types to limit the search results.
        :param name: Optional. A name fragment to search for.
        :param sort: Optional. The sorting criteria for the search results.
        :param permissions: Optional. If True, limits results to items with download permissions.
        :return: A QuickSearchResponse object containing the search results.
        """
        request_body = {
            'item_types': __item_type_request__(item_types),
            'filter': __wrap_filter_with_permissions__(search_filter).model_dump(
                exclude_none=True) if permissions else search_filter.model_dump(exclude_none=True)
        }
        if asset_types is not None:
            request_body['asset_types'] = asset_types
        if name is not None:
            request_body['name'] = name

        request_params = {'_page_size': self._page_size, '_sort': sort.value if sort else None}
        response_data = self._post(f'/quick-search', data=request_body, params=request_params)
        return QuickSearchResponse(features=self.__gather_features_from_response__(response_data))

    def activate_item_asset(self, item: QuickSearchItem, item_asset: str) -> ItemAsset:
        """
        Activates an item asset if its status is inactive. If the asset is already active or activating,
        the method does nothing. If the asset is inactive, the method sends a request to activate it.

        :param item: The QuickSearchItem that contains the asset to activate.
        :param item_asset: The ID of the item asset to activate.
        :return: An ItemAsset object representing the activated asset.
        :raises AssetNotFoundException: If the asset is not found in the item.
        """

        all_assets_response = self._get(item.links.assets)
        asset = all_assets_response.get(item_asset)
        if asset is None:
            raise AssetNotFoundException(item_asset)

        asset = ItemAsset(**asset)
        if asset.status == ItemAssetStatus.inactive:
            if self._session.get(asset.links.activate).status_code == 202:
                asset.status = ItemAssetStatus.activating

        return asset

    def check_asset_status(self, asset: ItemAsset) -> ItemAsset:
        """
        Checks the current status of an activated item asset by querying its status from the Planet API.

        :param asset: The ItemAsset object representing the asset whose status is being checked.
        :return: The updated ItemAsset object with the current status.
        """
        asset_data = self._get(asset.links.self)
        return ItemAsset(**asset_data)

    def download_item_asset(self, item_asset: ItemAsset, folder: str = None, filename: str = None) -> str:
        """
        Downloads an active item asset and saves it to the specified folder. If the asset is not active
        or does not have a valid location, a ValueError is raised.

        :param item_asset: The ItemAsset object representing the asset to download.
        :param folder: Optional. The folder where the asset will be saved. If not provided, the current directory is used.
        :param filename: Optional. The filename to save the asset as. If not provided, the filename is derived from the asset.
        :return: The file path where the asset was saved.
        :raises ValueError: If the item asset does not have a valid location.
        """
        if item_asset.location is None:
            raise ValueError('Failed to Download. This ItemAsset has no location.')

        return download_file(self._session, item_asset.location, folder, filename)

    def jupyter_preview(self, item: QuickSearchItem):
        """
        Displays a preview of the item's thumbnail image in a Jupyter notebook.

        This method fetches the thumbnail image from the Planet API and displays it using IPython's display functionality.

        :param item: The QuickSearchItem object representing the item to preview.
        :return: Displays the thumbnail image.
        """
        response = self._session.get(item.links.thumbnail, params={'width': 2048})
        image = Image.open(BytesIO(response.content))
        return display.display(image)

    def download_item_previews(self, items: List[QuickSearchItem], folder: str = ".") -> List[str]:
        """
        Gather and download a previews for a group of items
        :param items:
        :param folder:
        :return:
        """

        # Make sure the folder location exists
        os.makedirs(folder, exist_ok=True)

        paths = []
        for i in items:
            response = self._session.get(i.links.thumbnail, params={'width': 2048})
            # Build the full file path
            file_path = os.path.join(folder, f'{i.id}_preview.jpg')
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGB')
            image.save(file_path)
            paths.append(file_path)
        return paths
