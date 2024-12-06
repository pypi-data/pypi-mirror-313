from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, BaseModel

from cast_planet.orders.models.common import LinksBase
from cast_planet.orders.models.order_details import OrderState


class ResponseLinks(LinksBase):
    next: Optional[str] = Field(alias='_next', default=None)


class MosaicLinks(LinksBase):
    quads: str
    tiles: str


class MosaicGrid(BaseModel):
    quad_pattern: Optional[str] = None
    quad_size: float
    resolution: float


class Mosaic(BaseModel):
    links: MosaicLinks = Field(alias='_links')
    bands: Optional[int] = None
    bbox: List[float] = Field(min_length=4, max_length=4)
    coordinate_system: str
    datatype: Optional[str] = None
    first_acquired: datetime
    grid: Optional[MosaicGrid] = None
    id: UUID
    interval: str
    item_types: List[str]
    last_acquired: datetime
    level: int
    name: str
    product_type: str
    quad_download: bool = Field(default=False)


class MosaicsResponse(BaseModel):
    links: ResponseLinks = Field(alias='_links')
    mosaics: List[Mosaic]


class OrderStatus(BaseModel):
    state: OrderState
    last_message: str
