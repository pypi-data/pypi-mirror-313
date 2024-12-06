from typing import List

from cast_planet.data.filters.logical import AndFilter
from cast_planet.data.filters.base import BaseFilter


class PermissionFilter(BaseFilter):
    """
    Limits search results to items the user has permission to download.
    This filter is added by default for all searches.

    IMPORTANT: Not recommended for use with logical 'Or' or 'Not' filters. Use of these without an 'And' filter will
    void the permissions' requirement.
    """
    config: List[str] = [
        "assets:download"
    ]
    """ This is automatically set to 'assets:download'. Do not change. """


def __wrap_filter_with_permissions__(user_provided_filter: BaseFilter):
    return AndFilter(config=[user_provided_filter, PermissionFilter()])