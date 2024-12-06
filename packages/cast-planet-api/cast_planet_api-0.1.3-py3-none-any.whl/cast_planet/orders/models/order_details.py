from datetime import datetime
from enum import Enum
from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field

from cast_planet.orders.models.common import LinksBase
from cast_planet.orders.models.order_hosting import CouldHaveHosting
from cast_planet.orders.models.order_delivery import OrderDelivery
from cast_planet.orders.models.order_notifications import OrderNotifications
from cast_planet.orders.models.order_products import CouldHaveOrderProducts
from cast_planet.orders.models.tools import HasToolsList


class ResultState(Enum):
    PENDING = "pending"
    FAILED = "failed"
    SUCCESS = "success"


class OrderResult(BaseModel):
    delivery: ResultState
    name: Optional[str] = None
    location: Optional[str] = None
    expires_at: Optional[datetime] = None


class OrderDetailsLinks(LinksBase):
    results: Optional[List[OrderResult]] = None


class OrderState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    FAILED = "failed"
    SUCCESS = "success"
    PARTIAL = "partial"
    CANCELLED = "cancelled"


class OrderMetadata(BaseModel):
    stac: Optional[Any] = None


class OrderDetails(HasToolsList, CouldHaveHosting, CouldHaveOrderProducts):
    links: Optional[OrderDetailsLinks] = Field(alias='_links', default=None)
    id: UUID
    name: str
    subscription_id: Optional[int] = 0
    metadata: Optional[OrderMetadata] = None
    created_on: datetime
    last_modified: datetime
    state: OrderState
    last_message: str
    error_hints: List[str]
    delivery: Optional[OrderDelivery] = None
    notifications: Optional[OrderNotifications] = None
    order_type: str
    source_type: str

    def print_info(self):
        print(f"NAME:{self.name}\nSTATUS: {self.state} - {self.last_message}")
