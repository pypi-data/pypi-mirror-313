from typing import List

from pydantic import Field

from cast_planet.data.filters.base import BaseFilter


class AssetFilter(BaseFilter):
    """

    From the asset filter documentation:

    The filter's configuration is a list of asset types. When multiple values are specified,
    an implicit “or” logic is applied, returning all items which include any of the listed asset
    types. An AndFilter can be used to filter items by multiple asset types.
    https://developers.planet.com/docs/apis/data/searches-filtering/#asset-filters
    """
    config: List[str] = Field(min_length=1, description='A list of item assets.', examples=['ortho_analytics_4b'])