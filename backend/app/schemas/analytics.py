"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal


# Analytics Schemas

class DateRangeFilter(BaseModel):
    """Date range filter for analytics queries"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class DimensionFilter(BaseModel):
    """Filter by various dimensions"""
    store_ids: Optional[List[int]] = None
    channel_ids: Optional[List[int]] = None
    product_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None
    customer_ids: Optional[List[int]] = None
    sale_status: Optional[List[str]] = None


class AnalyticsRequest(BaseModel):
    """Generic analytics request"""
    date_range: Optional[DateRangeFilter] = None
    filters: Optional[DimensionFilter] = None
    group_by: Optional[List[str]] = None
    metrics: Optional[List[str]] = None
    limit: Optional[int] = 100


# Response Schemas

class SalesOverviewResponse(BaseModel):
    """Sales overview metrics"""
    total_sales: int
    total_revenue: float
    average_ticket: float
    completed_sales: int
    cancelled_sales: int
    total_discount: float
    total_delivery_fee: float
    
    class Config:
        from_attributes = True


class ProductRankingItem(BaseModel):
    """Product ranking item"""
    product_id: int
    product_name: str
    category_name: Optional[str] = None
    total_quantity: float
    total_revenue: float
    order_count: int
    average_price: float


class ProductRankingResponse(BaseModel):
    """Product ranking response"""
    products: List[ProductRankingItem]
    total_count: int


class ChannelPerformanceItem(BaseModel):
    """Channel performance metrics"""
    channel_id: int
    channel_name: str
    channel_type: str
    total_sales: int
    total_revenue: float
    average_ticket: float
    revenue_percentage: float


class ChannelPerformanceResponse(BaseModel):
    """Channel performance response"""
    channels: List[ChannelPerformanceItem]


class StorePerformanceItem(BaseModel):
    """Store performance metrics"""
    store_id: int
    store_name: str
    city: Optional[str] = None
    state: Optional[str] = None
    total_sales: int
    total_revenue: float
    average_ticket: float
    revenue_percentage: float


class StorePerformanceResponse(BaseModel):
    """Store performance response"""
    stores: List[StorePerformanceItem]


class TimeSeriesDataPoint(BaseModel):
    """Time series data point"""
    date: str
    sales_count: int
    revenue: float
    average_ticket: float


class TimeSeriesResponse(BaseModel):
    """Time series response"""
    data: List[TimeSeriesDataPoint]
    period_type: str  # daily, weekly, monthly


class CustomerRetentionItem(BaseModel):
    """Customer retention analysis"""
    customer_id: int
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    total_orders: int
    total_spent: float
    average_ticket: float
    last_order_date: datetime
    days_since_last_order: int
    first_order_date: datetime


class CustomerRetentionResponse(BaseModel):
    """Customer retention response"""
    customers: List[CustomerRetentionItem]
    total_count: int


class DeliveryPerformanceItem(BaseModel):
    """Delivery performance metrics"""
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    total_deliveries: int
    avg_delivery_time_minutes: float
    avg_production_time_minutes: float
    total_delivery_time_minutes: float


class DeliveryPerformanceResponse(BaseModel):
    """Delivery performance response"""
    performance: List[DeliveryPerformanceItem]


class HourlyPerformanceItem(BaseModel):
    """Hourly performance metrics"""
    hour: int
    day_of_week: Optional[int] = None
    day_name: Optional[str] = None
    sales_count: int
    revenue: float
    average_ticket: float


class HourlyPerformanceResponse(BaseModel):
    """Hourly performance response"""
    performance: List[HourlyPerformanceItem]


class ProductMarginItem(BaseModel):
    """Product margin analysis"""
    product_id: int
    product_name: str
    category_name: Optional[str] = None
    avg_base_price: float
    avg_total_price: float
    avg_customization_value: float
    total_revenue: float
    order_count: int


class ProductMarginResponse(BaseModel):
    """Product margin response"""
    products: List[ProductMarginItem]


class CustomQueryResponse(BaseModel):
    """Flexible custom query response"""
    data: List[Dict[str, Any]]
    columns: List[str]
    total_count: int
    query_time_ms: float


# Dashboard Schemas

class DashboardMetric(BaseModel):
    """Single dashboard metric"""
    label: str
    value: Any
    change_percentage: Optional[float] = None
    format_type: str = "number"  # number, currency, percentage, duration


class DashboardWidget(BaseModel):
    """Dashboard widget configuration"""
    widget_type: str  # metric, chart, table
    title: str
    data: Any
    config: Optional[Dict[str, Any]] = None


class DashboardResponse(BaseModel):
    """Complete dashboard response"""
    name: str
    description: Optional[str] = None
    widgets: List[DashboardWidget]
    last_updated: datetime


# Metadata Schemas

class StoreInfo(BaseModel):
    """Store information"""
    id: int
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    is_active: bool


class ChannelInfo(BaseModel):
    """Channel information"""
    id: int
    name: str
    type: str
    description: Optional[str] = None


class ProductInfo(BaseModel):
    """Product information"""
    id: int
    name: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None


class CategoryInfo(BaseModel):
    """Category information"""
    id: int
    name: str
    type: str


class MetadataResponse(BaseModel):
    """Metadata response with all dimensions"""
    stores: List[StoreInfo]
    channels: List[ChannelInfo]
    categories: List[CategoryInfo]
