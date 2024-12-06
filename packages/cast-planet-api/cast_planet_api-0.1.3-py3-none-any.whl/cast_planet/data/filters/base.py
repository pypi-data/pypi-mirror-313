from abc import ABC
from typing import Optional, Any

from pydantic import BaseModel, model_validator, Field


class BaseFilter(BaseModel, ABC):
    """
    Base filter for creating Data API filters.

    Be sure any subclasses created from this filter match the
    type naming conventions from https://developers.planet.com/docs/apis/data/searches-filtering/

    """
    type: Optional[str] = Field(..., title='type', description='The type of filter being created. This is '
                                                               'automatically generated. Do not alter.')

    @model_validator(mode="before")
    @classmethod
    def set_type(cls, values):
        values["type"] = cls.__name__
        return values