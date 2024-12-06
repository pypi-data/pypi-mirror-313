"""
Learn more about each individual Field search filter at
https://developers.planet.com/docs/apis/data/searches-filtering/#field-filters
"""

from datetime import datetime
from typing import Optional, List, Union, Annotated

from pydantic import BaseModel, Field, field_validator, PlainSerializer
from pydantic_geojson import PointModel, MultiPointModel, LineStringModel, MultiLineStringModel, \
    PolygonModel, MultiPolygonModel

from cast_planet.data.filters.base import BaseFilter


def serialize_optional_date(value : Union[datetime, None]):
    if value is None:
        return ''  # or any other desired representation for None values
    return str(value.strftime("%Y-%m-%dT%H:%M:%SZ"))  # Serialize the value if it's not None


DateTimeField = Annotated[
    datetime,
    PlainSerializer(lambda _datetime: serialize_optional_date(_datetime), return_type=str),
]


class BaseFieldFilter(BaseFilter):
    field_name: str


class DateRangeConfig(BaseModel):
    gt: Optional[Union[DateTimeField, str]] = Field(default=None, title='gt', description='Greater than')
    lt: Optional[Union[DateTimeField, str]] = None
    gte: Optional[Union[DateTimeField, str]] = None
    lte: Optional[Union[DateTimeField, str]] = None

    # Field validators to parse strings into datetime objects
    @field_validator("gt", "lt", "gte", "lte", mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class DateRangeFilter(BaseFieldFilter):
    config: DateRangeConfig


class GeometryFilter(BaseFieldFilter):
    """
    Matches items with a footprint that intersects with a specified GeoJSON geometry.

    :param config: A valid GeJSON feature dictionary.
    """
    config: Union[
        PointModel,
        MultiPointModel,
        LineStringModel,
        MultiLineStringModel,
        PolygonModel,
        MultiPolygonModel,
    ]


class NumberInFilter(BaseFieldFilter):
    config: List[Union[int, float]] = Field(min_length=1)


class RangeConfig(BaseModel):
    lt: Optional[Union[int, float]] = None
    gte: Optional[Union[int, float]] = None
    lte: Optional[Union[int, float]] = None


class RangeFilter(BaseFieldFilter):
    config: RangeConfig


class StringInFilter(BaseFieldFilter):
    config: List[str] = Field(min_length=1)


class UpdateConfig(BaseFieldFilter):
    gt: Optional[Union[int, float]]
    gte: Optional[Union[int, float]]


class UpdateFilter(BaseFieldFilter):
    config: UpdateConfig
