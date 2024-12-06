from enum import Enum

from pydantic import BaseModel, Field


class LinksBase(BaseModel):
    self: str = Field(alias='_self')


class OrderType(str, Enum):
    FULL = 'full'
    PARTIAL = 'partial'


class OrderSource(str, Enum):
    SCENE = 'scenes'
    BASEMAP = 'basemaps'
