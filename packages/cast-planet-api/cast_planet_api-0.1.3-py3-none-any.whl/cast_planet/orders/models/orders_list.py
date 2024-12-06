from typing import List, Optional

from pydantic import BaseModel, Field

from cast_planet.orders.models.order_details import OrderDetails


class OrdersResponseLinks(BaseModel):
    self: str = Field(alias='_self')
    next: Optional[str] = None


class OrdersResponse(BaseModel):
    links: OrdersResponseLinks = Field(alias='_links')
    orders: List[OrderDetails]
