from typing import List, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class TopProductItem(BaseModel):
    product_id: int
    product_name: str
    quantity: float


class TicketTrendPoint(BaseModel):
    group_by: str
    period_start: str
    avg_ticket: float


class DeliveryPerfPoint(BaseModel):
    day_of_week: int
    hour: Optional[int]
    avg_delivery_seconds: Optional[float]


class ChurnedCustomer(BaseModel):
    customer_id: Optional[int]
    customer_name: Optional[str]
    last_order_at: Optional[str]
    orders_count: int
