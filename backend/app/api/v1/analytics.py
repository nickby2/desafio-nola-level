"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    DateRangeFilter, DimensionFilter,
    SalesOverviewResponse, ProductRankingResponse,
    ChannelPerformanceResponse, StorePerformanceResponse,
    TimeSeriesResponse, CustomerRetentionResponse,
    DeliveryPerformanceResponse, HourlyPerformanceResponse,
    ProductMarginResponse
)

router = APIRouter()


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    """Dependency for analytics service"""
    return AnalyticsService(db)


@router.get("/overview", response_model=SalesOverviewResponse)
def get_sales_overview(
    start_date: Optional[datetime] = Query(None, description="Start date for filter"),
    end_date: Optional[datetime] = Query(None, description="End date for filter"),
    store_ids: Optional[str] = Query(None, description="Comma-separated store IDs"),
    channel_ids: Optional[str] = Query(None, description="Comma-separated channel IDs"),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get overall sales metrics
    
    Returns total sales, revenue, average ticket, completed/cancelled counts, etc.
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    return service.get_sales_overview(date_range=date_range, filters=filters)


@router.get("/products/ranking", response_model=ProductRankingResponse)
def get_product_ranking(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    store_ids: Optional[str] = Query(None),
    channel_ids: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get top selling products
    
    Returns products ranked by quantity sold, with revenue and order count.
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    products = service.get_product_ranking(
        date_range=date_range, 
        filters=filters, 
        limit=limit
    )
    
    return ProductRankingResponse(products=products, total_count=len(products))


@router.get("/channels/performance", response_model=ChannelPerformanceResponse)
def get_channel_performance(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    store_ids: Optional[str] = Query(None),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get performance metrics by sales channel
    
    Answers: "Meu ticket médio está caindo. É por canal ou por loja?"
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    
    channels = service.get_channel_performance(date_range=date_range, filters=filters)
    
    return ChannelPerformanceResponse(channels=channels)


@router.get("/stores/performance", response_model=StorePerformanceResponse)
def get_store_performance(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    channel_ids: Optional[str] = Query(None),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get performance metrics by store
    
    Answers: "Meu ticket médio está caindo. É por canal ou por loja?"
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    stores = service.get_store_performance(date_range=date_range, filters=filters)
    
    return StorePerformanceResponse(stores=stores)


@router.get("/timeseries", response_model=TimeSeriesResponse)
def get_time_series(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    period: str = Query('daily', regex='^(daily|weekly|monthly)$'),
    store_ids: Optional[str] = Query(None),
    channel_ids: Optional[str] = Query(None),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get sales time series data
    
    Returns sales metrics over time (daily, weekly, or monthly).
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    data = service.get_time_series(
        date_range=date_range, 
        filters=filters, 
        period=period
    )
    
    return TimeSeriesResponse(data=data, period_type=period)


@router.get("/customers/retention", response_model=CustomerRetentionResponse)
def get_customer_retention(
    min_orders: int = Query(3, ge=1, description="Minimum orders to include"),
    days_inactive: int = Query(30, ge=1, description="Days since last order"),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get customers at risk of churning
    
    Answers: "Quais clientes compraram 3+ vezes mas não voltam há 30 dias?"
    """
    customers = service.get_customer_retention(
        min_orders=min_orders,
        days_inactive=days_inactive
    )
    
    return CustomerRetentionResponse(customers=customers, total_count=len(customers))


@router.get("/delivery/performance", response_model=DeliveryPerformanceResponse)
def get_delivery_performance(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    store_ids: Optional[str] = Query(None),
    channel_ids: Optional[str] = Query(None),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get delivery performance by location
    
    Answers: "Meu tempo de entrega piorou. Em quais dias/horários?"
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    performance = service.get_delivery_performance(date_range=date_range, filters=filters)
    
    return DeliveryPerformanceResponse(performance=performance)


@router.get("/hourly/performance", response_model=HourlyPerformanceResponse)
def get_hourly_performance(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    day_of_week: Optional[int] = Query(None, ge=0, le=6, description="Day of week (0=Sunday, 4=Thursday)"),
    store_ids: Optional[str] = Query(None),
    channel_ids: Optional[str] = Query(None),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get performance by hour and day of week
    
    Answers: "Qual produto vende mais na quinta à noite no iFood?"
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    performance = service.get_hourly_performance(
        date_range=date_range,
        filters=filters,
        day_of_week=day_of_week
    )
    
    return HourlyPerformanceResponse(performance=performance)


@router.get("/products/margin", response_model=ProductMarginResponse)
def get_product_margin_analysis(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    store_ids: Optional[str] = Query(None),
    channel_ids: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get product margin analysis
    
    Answers: "Quais produtos têm menor margem e devo repensar o preço?"
    Shows base price vs actual price with customizations.
    """
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date)
    
    filters = DimensionFilter()
    if store_ids:
        filters.store_ids = [int(x) for x in store_ids.split(',')]
    if channel_ids:
        filters.channel_ids = [int(x) for x in channel_ids.split(',')]
    
    products = service.get_product_margin_analysis(
        date_range=date_range,
        filters=filters,
        limit=limit
    )
    
    return ProductMarginResponse(products=products)
