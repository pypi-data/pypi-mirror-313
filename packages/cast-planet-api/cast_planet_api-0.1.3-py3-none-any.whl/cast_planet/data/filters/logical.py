from typing import List, Any, Dict

from pydantic import Field, model_validator, validator, field_validator

from cast_planet.data.filters.base import BaseFilter


class LogicFilter(BaseFilter):
    config: List[Any] = Field(min_length=1, description="A list of objects to which this logic will apply.")

    @model_validator(mode='before')
    @classmethod
    def validate_config_filters(cls, v: Dict[str,Any]):
        for i in v['config']:
            if not issubclass(type(i), BaseFilter):
                raise ValueError(f'Must be sublclass of {BaseFilter.__name__}')
        return v


class AndFilter(LogicFilter):
    """
    Matches items with properties or permissions which match all the nested filters.

    See more at:
    https://developers.planet.com/docs/apis/data/searches-filtering/#logical-filters
    """
    pass


class OrFilter(LogicFilter):
    """
    Matches items with properties or permissions which match at least one of the nested filters.

    See more at:
    https://developers.planet.com/docs/apis/data/searches-filtering/#logical-filters
    """
    pass


class NotFilter(BaseFilter):
    """
    Matches items with properties or permissions which do not match the nested
    filter. This filter type supports a single nested filter.


    See more at:
    https://developers.planet.com/docs/apis/data/searches-filtering/#logical-filters
    """
    config: BaseFilter
