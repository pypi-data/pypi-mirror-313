from typing import Optional

from pydantic import Field

from cast_planet.orders.models.common import OrderType, OrderSource
from cast_planet.orders.models.order_delivery import OrderDelivery
from cast_planet.orders.models.order_hosting import CouldHaveHosting
from cast_planet.orders.models.order_notifications import OrderNotifications
from cast_planet.orders.models.order_products import CouldHaveOrderProducts
from cast_planet.orders.models.tools import CouldHaveToolsList


class CreateOrder(CouldHaveToolsList, CouldHaveOrderProducts, CouldHaveHosting):
    name: str = Field(description='A name given to this Order request.')
    subscription_id: Optional[int] = Field(description='apply this orders against this quota subscription',
                                           default=None)
    delivery: Optional[OrderDelivery] = Field(description="How should ordered products be delivered?", default=None)
    notifications: Optional[OrderNotifications] = Field(
        description="How would you like to be notified when order is complete?", default=None)
    order_type: OrderType = Field(default=OrderType.PARTIAL,
                                  description="accept order if requested products are not available (partial)?")
    source_type: Optional[OrderSource] = Field(default=None,
                                               description='Source imagery type for all products. Default is scenes.')