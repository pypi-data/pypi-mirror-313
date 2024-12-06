from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SentinelHubHosting(BaseModel):
    """
    Before using, you must follow the steps in this article: Linking Planet User to Sentinel Hub User.
    https://support.planet.com/hc/en-us/articles/16417885928221-Linking-Planet-User-to-Sentinel-Hub-User

    Collections can be found on the Sentinel Hub Dashboard.
    https://apps.sentinel-hub.com/dashboard/#/collections
    """
    collection_id: UUID = Field(description="A Sentinel Hub BYOC collection to deliver to. If omitted, a new "
                                            "collection will be created for you and returned in the response")


class OrderHosting(BaseModel):
    sentinel_hub: SentinelHubHosting


class CouldHaveHosting(BaseModel):
    hosting: Optional[OrderHosting] = None
