from typing import List, Optional, Union

from pydantic import BaseModel, Field
from pydantic_geojson import PointModel, PolygonModel, MultiPolygonModel


class SceneSource(BaseModel):
    item_ids: List[str] = Field(description='Array of item ids.')
    item_type: str = Field(description='item-type for requested item_id.')
    product_bundle: str = Field(description='asset-type for the item.')


# Basemap sources cannot handle having both the geometry parameter
# and the quad_id parameter exist at the same time.
# We will create separate objects for each use case.
class BaseMapsGeometrySource(BaseModel):
    mosaic_name: str = Field(description='Name of mosaic')

    geometry: Optional[Union[PointModel, PolygonModel, MultiPolygonModel]] = Field(default=None,
                                                                                   description='GeoJSON object.')


class BaseMapsQuadIdSource(BaseModel):
    mosaic_name: str = Field(description='Name of mosaic')
    quad_ids: Optional[List[str]] = Field(default=[], description='List of quad ids.')


_product_description = 'The products from the Data or Basemaps API to order.'


class CouldHaveOrderProducts(BaseModel):
    products: Optional[List[Union[SceneSource, BaseMapsGeometrySource, BaseMapsQuadIdSource]]] \
        = Field(default=None, description=_product_description)
