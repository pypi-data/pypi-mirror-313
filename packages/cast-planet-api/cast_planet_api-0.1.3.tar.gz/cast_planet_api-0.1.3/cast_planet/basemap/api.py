from typing import List
from uuid import UUID

from cast_planet._utils._base_api import BaseApi
from cast_planet.basemap.models import MosaicsResponse, Mosaic


class BasemapApi(BaseApi):
    def __init__(self, api_key: str, base_url: str = 'https://api.planet.com/basemaps/v1'):
        """
        Initializes the BasemapApi class by calling the constructor of the BaseApi class.

        This class provides methods to interact with the Basemap API, including listing mosaics, searching mosaics by name,
        and fetching mosaics by their unique ID.

        :param api_key: The API key used for authentication with the Planet API.
        :param base_url: The base URL for the Basemap API (default is 'https://api.planet.com/basemaps/v1').
        """
        super().__init__(api_key, base_url)

    def __gather_mosaics_from_response__(self, mosaics_response: MosaicsResponse) -> List[Mosaic]:
        """
        Collects all mosaics by following the pagination links in the response, combining results from multiple pages.

        This helper method is used to gather all mosaics, including those from subsequent pages,
        by checking the 'next' link in the response and making additional GET requests if necessary.

        :param mosaics_response: The initial response from the Basemap API containing a list of mosaics and pagination links.
        :return: A list of all mosaics retrieved from the API, potentially spanning multiple pages.
        :rtype: List[Mosaic]
        """
        mosaics = mosaics_response.mosaics
        while mosaics_response.links.next is not None:
            mosaics_response_data = self._get(mosaics_response.links.next)
            mosaics_response = MosaicsResponse(**mosaics_response_data)
            mosaics.extend(mosaics_response.mosaics)  # Add the new mosaics to the existing list
        return mosaics

    def list_mosaics(self) -> List[Mosaic]:
        """
        Retrieves a list of all available mosaics from the Basemap API.

        This method fetches all mosaics available through the Basemap API, potentially making multiple requests
        if pagination is involved.

        :return: A list of mosaics available in the Basemap API.
        :rtype: List[Mosaic]
        """
        mosaics_response_data = self._get(f"/mosaics")
        mosaics_response = MosaicsResponse(**mosaics_response_data)
        return self.__gather_mosaics_from_response__(mosaics_response)

    def search_mosaics(self, name_contains: str) -> List[Mosaic]:
        """
        Searches for mosaics based on a partial match of their name.

        This method queries the Basemap API for mosaics whose names contain the provided string
        and returns a list of matching mosaics.

        :param name_contains: A string that the mosaic names should contain. The search is case-sensitive.
        :return: A list of mosaics whose names contain the search string.
        :rtype: List[Mosaic]
        """
        params = {'name__contains': name_contains}
        mosaics_response_data = self._get(f"/mosaics", params=params)
        mosaics_response = MosaicsResponse(**mosaics_response_data)
        return self.__gather_mosaics_from_response__(mosaics_response)

    def get_mosaic_by_id(self, mosaic_id: UUID) -> Mosaic:
        """
        Retrieves a specific mosaic by its unique ID.

        This method fetches details of a mosaic from the Basemap API by providing its unique identifier (UUID).

        :param mosaic_id: The unique identifier of the mosaic to retrieve.
        :return: A Mosaic object containing the details of the specified mosaic.
        :rtype: Mosaic
        """
        mosaic_data = self._get(f'/mosaics/{mosaic_id}')
        return Mosaic(**mosaic_data)
