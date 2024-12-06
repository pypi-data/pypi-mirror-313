from enum import Enum
from typing import Callable, List, Any, Dict, Optional
from datetime import datetime

from pydantic import Field, BaseModel, model_validator
from pydantic_geojson import FeatureCollectionModel, FeatureModel


class ItemType(BaseModel):
    """

    """
    id: str
    display_description: str
    display_name: str
    supported_asset_types: List[str]


class Links(BaseModel):
    self: str = Field(alias='_self')
    first: str = Field(alias='_first')
    next: str = Field(alias='_next')


class FeatureLinks(BaseModel):
    self: str = Field(alias='_self')
    assets: str
    thumbnail: str


class QuerySort(Enum):
    """
    Supported values for the _sort query parameter.
    Default value if none specified is published desc
    """
    AcquiredAsc = 'acquired asc',
    AcquiredDesc = 'acquired desc',
    PublishedAsc = 'published asc',
    PublishedDesc = 'published desc'


class ItemAssetStatus(Enum):
    inactive = 'inactive'
    activating = 'activating'
    active = 'active'


class ItemAssetLinks(BaseModel):
    self: str = Field(alias='_self')
    activate: str
    type: str


class ItemAsset(BaseModel):
    links: ItemAssetLinks = Field(alias="_links")
    permissions: List[str] = Field(alias='_permissions')
    expires_at: Optional[datetime] = None
    location: Optional[str] = None
    status: ItemAssetStatus
    type: str


class QuickSearchItem(FeatureModel):
    links: FeatureLinks = Field(alias='_links')
    permissions: List[str] = Field(alias='_permissions')
    properties: Dict[str, Any]
    assets: List[str]
    id: str

    @model_validator(mode='before')
    @classmethod
    def convert_time_properties(cls, v: Dict[str, Any]):
        for i in v['properties']:
            if isinstance(i, str):
                try:
                    v['properties'][i] = datetime.strptime(v['properties'][i], "%Y-%m-%dT%H:%M:%S.%fZ")
                except Exception as e:
                    pass
        return v


class QuickSearchResponse(FeatureCollectionModel):
    features: List[QuickSearchItem]
    """A list of QuickSearchItem(s) returned from the REST API."""

    def filter(self, func: Callable[[QuickSearchItem], bool]):
        """
        Filter results by a custom comparer.

        Args:
            func: Any function that takes in a ResponseFeature and returns a boolean result.
        """
        return_features = list()
        for f in self.features:
            if func(f):
                return_features.append(f)
        return return_features

    @property
    def count(self):
        """ A count of all features returned from the search."""
        return len(self.features)