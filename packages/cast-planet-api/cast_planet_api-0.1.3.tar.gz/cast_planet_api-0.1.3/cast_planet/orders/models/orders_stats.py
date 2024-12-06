from pydantic import BaseModel


class ActiveOrderStats(BaseModel):
    queued_orders: int
    running_orders: int


class OrdersStats(BaseModel):
    user: ActiveOrderStats
    organization: ActiveOrderStats
