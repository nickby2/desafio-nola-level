"""
Analytics service - Core business logic for restaurant analytics
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, cast, Date, extract, case
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.models.models import (
    Sale, Store, Channel, Product, ProductSale, Customer,
    Category, DeliveryAddress, DeliverySale
)
from app.schemas.analytics import (
    DateRangeFilter, DimensionFilter,
    SalesOverviewResponse, ProductRankingItem, ChannelPerformanceItem,
    StorePerformanceItem, TimeSeriesDataPoint, CustomerRetentionItem,
    DeliveryPerformanceItem, HourlyPerformanceItem, ProductMarginItem
)


class AnalyticsService:
    """Analytics service for restaurant data"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _apply_filters(self, query, date_range: Optional[DateRangeFilter] = None,
                      filters: Optional[DimensionFilter] = None):
        """Apply common filters to a query"""
        if date_range:
            if date_range.start_date:
                query = query.filter(Sale.created_at >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Sale.created_at <= date_range.end_date)
        
        if filters:
            if filters.store_ids:
                query = query.filter(Sale.store_id.in_(filters.store_ids))
            if filters.channel_ids:
                query = query.filter(Sale.channel_id.in_(filters.channel_ids))
            if filters.sale_status:
                query = query.filter(Sale.sale_status_desc.in_(filters.sale_status))
            if filters.customer_ids:
                query = query.filter(Sale.customer_id.in_(filters.customer_ids))
        
        return query
    
    def get_sales_overview(self, date_range: Optional[DateRangeFilter] = None,
                          filters: Optional[DimensionFilter] = None) -> SalesOverviewResponse:
        """Get overall sales metrics"""
        query = self.db.query(
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.total_amount).label('total_revenue'),
            func.avg(Sale.total_amount).label('average_ticket'),
            func.sum(case((Sale.sale_status_desc == 'COMPLETED', 1), else_=0)).label('completed_sales'),
            func.sum(case((Sale.sale_status_desc == 'CANCELLED', 1), else_=0)).label('cancelled_sales'),
            func.sum(Sale.total_discount).label('total_discount'),
            func.sum(Sale.delivery_fee).label('total_delivery_fee')
        )
        
        query = self._apply_filters(query, date_range, filters)
        result = query.first()
        
        return SalesOverviewResponse(
            total_sales=result.total_sales or 0,
            total_revenue=float(result.total_revenue or 0),
            average_ticket=float(result.average_ticket or 0),
            completed_sales=result.completed_sales or 0,
            cancelled_sales=result.cancelled_sales or 0,
            total_discount=float(result.total_discount or 0),
            total_delivery_fee=float(result.total_delivery_fee or 0)
        )
    
    def get_product_ranking(self, date_range: Optional[DateRangeFilter] = None,
                           filters: Optional[DimensionFilter] = None,
                           limit: int = 20) -> List[ProductRankingItem]:
        """Get top selling products"""
        query = self.db.query(
            Product.id.label('product_id'),
            Product.name.label('product_name'),
            Category.name.label('category_name'),
            func.sum(ProductSale.quantity).label('total_quantity'),
            func.sum(ProductSale.total_price).label('total_revenue'),
            func.count(func.distinct(Sale.id)).label('order_count'),
            func.avg(ProductSale.total_price / ProductSale.quantity).label('average_price')
        ).select_from(ProductSale)\
         .join(Product, ProductSale.product_id == Product.id)\
         .join(Sale, ProductSale.sale_id == Sale.id)\
         .outerjoin(Category, Product.category_id == Category.id)
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(Sale.sale_status_desc == 'COMPLETED')
        query = query.group_by(Product.id, Product.name, Category.name)
        query = query.order_by(func.sum(ProductSale.quantity).desc())
        query = query.limit(limit)
        
        results = query.all()
        
        return [
            ProductRankingItem(
                product_id=r.product_id,
                product_name=r.product_name,
                category_name=r.category_name,
                total_quantity=float(r.total_quantity or 0),
                total_revenue=float(r.total_revenue or 0),
                order_count=r.order_count or 0,
                average_price=float(r.average_price or 0)
            )
            for r in results
        ]
    
    def get_channel_performance(self, date_range: Optional[DateRangeFilter] = None,
                               filters: Optional[DimensionFilter] = None) -> List[ChannelPerformanceItem]:
        """Get performance by sales channel"""
        # Get total revenue for percentage calculation
        total_revenue_query = self.db.query(
            func.sum(Sale.total_amount).label('total')
        )
        total_revenue_query = self._apply_filters(total_revenue_query, date_range, filters)
        total_revenue_query = total_revenue_query.filter(Sale.sale_status_desc == 'COMPLETED')
        total_revenue = total_revenue_query.scalar() or 0
        
        query = self.db.query(
            Channel.id.label('channel_id'),
            Channel.name.label('channel_name'),
            Channel.type.label('channel_type'),
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.total_amount).label('total_revenue'),
            func.avg(Sale.total_amount).label('average_ticket')
        ).select_from(Sale)\
         .join(Channel, Sale.channel_id == Channel.id)
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(Sale.sale_status_desc == 'COMPLETED')
        query = query.group_by(Channel.id, Channel.name, Channel.type)
        query = query.order_by(func.sum(Sale.total_amount).desc())
        
        results = query.all()
        
        return [
            ChannelPerformanceItem(
                channel_id=r.channel_id,
                channel_name=r.channel_name,
                channel_type=r.channel_type,
                total_sales=r.total_sales or 0,
                total_revenue=float(r.total_revenue or 0),
                average_ticket=float(r.average_ticket or 0),
                revenue_percentage=float((r.total_revenue / total_revenue * 100) if total_revenue > 0 else 0)
            )
            for r in results
        ]
    
    def get_store_performance(self, date_range: Optional[DateRangeFilter] = None,
                            filters: Optional[DimensionFilter] = None) -> List[StorePerformanceItem]:
        """Get performance by store"""
        # Get total revenue for percentage calculation
        total_revenue_query = self.db.query(
            func.sum(Sale.total_amount).label('total')
        )
        total_revenue_query = self._apply_filters(total_revenue_query, date_range, filters)
        total_revenue_query = total_revenue_query.filter(Sale.sale_status_desc == 'COMPLETED')
        total_revenue = total_revenue_query.scalar() or 0
        
        query = self.db.query(
            Store.id.label('store_id'),
            Store.name.label('store_name'),
            Store.city,
            Store.state,
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.total_amount).label('total_revenue'),
            func.avg(Sale.total_amount).label('average_ticket')
        ).select_from(Sale)\
         .join(Store, Sale.store_id == Store.id)
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(Sale.sale_status_desc == 'COMPLETED')
        query = query.group_by(Store.id, Store.name, Store.city, Store.state)
        query = query.order_by(func.sum(Sale.total_amount).desc())
        
        results = query.all()
        
        return [
            StorePerformanceItem(
                store_id=r.store_id,
                store_name=r.store_name,
                city=r.city,
                state=r.state,
                total_sales=r.total_sales or 0,
                total_revenue=float(r.total_revenue or 0),
                average_ticket=float(r.average_ticket or 0),
                revenue_percentage=float((r.total_revenue / total_revenue * 100) if total_revenue > 0 else 0)
            )
            for r in results
        ]
    
    def get_time_series(self, date_range: Optional[DateRangeFilter] = None,
                       filters: Optional[DimensionFilter] = None,
                       period: str = 'daily') -> List[TimeSeriesDataPoint]:
        """Get sales time series data"""
        if period == 'daily':
            date_group = cast(Sale.created_at, Date)
        elif period == 'weekly':
            # Group by week
            date_group = func.date_trunc('week', Sale.created_at)
        elif period == 'monthly':
            # Group by month
            date_group = func.date_trunc('month', Sale.created_at)
        else:
            date_group = cast(Sale.created_at, Date)
        
        query = self.db.query(
            date_group.label('date'),
            func.count(Sale.id).label('sales_count'),
            func.sum(Sale.total_amount).label('revenue'),
            func.avg(Sale.total_amount).label('average_ticket')
        )
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(Sale.sale_status_desc == 'COMPLETED')
        query = query.group_by(date_group)
        query = query.order_by(date_group)
        
        results = query.all()
        
        return [
            TimeSeriesDataPoint(
                date=r.date.isoformat() if hasattr(r.date, 'isoformat') else str(r.date),
                sales_count=r.sales_count or 0,
                revenue=float(r.revenue or 0),
                average_ticket=float(r.average_ticket or 0)
            )
            for r in results
        ]
    
    def get_customer_retention(self, min_orders: int = 3, days_inactive: int = 30,
                              date_range: Optional[DateRangeFilter] = None) -> List[CustomerRetentionItem]:
        """Get customers at risk of churning (bought 3+ times but haven't returned in X days)"""
        cutoff_date = datetime.now() - timedelta(days=days_inactive)
        
        # Subquery to get customer stats
        customer_stats = self.db.query(
            Sale.customer_id,
            func.count(Sale.id).label('total_orders'),
            func.sum(Sale.total_amount).label('total_spent'),
            func.avg(Sale.total_amount).label('average_ticket'),
            func.max(Sale.created_at).label('last_order_date'),
            func.min(Sale.created_at).label('first_order_date')
        ).filter(
            Sale.customer_id.isnot(None),
            Sale.sale_status_desc == 'COMPLETED'
        ).group_by(Sale.customer_id).subquery()
        
        query = self.db.query(
            Customer.id.label('customer_id'),
            Customer.customer_name,
            Customer.email,
            Customer.phone_number,
            customer_stats.c.total_orders,
            customer_stats.c.total_spent,
            customer_stats.c.average_ticket,
            customer_stats.c.last_order_date,
            customer_stats.c.first_order_date
        ).join(customer_stats, Customer.id == customer_stats.c.customer_id)\
         .filter(
            customer_stats.c.total_orders >= min_orders,
            customer_stats.c.last_order_date < cutoff_date
        ).order_by(customer_stats.c.total_spent.desc())
        
        results = query.all()
        
        return [
            CustomerRetentionItem(
                customer_id=r.customer_id,
                customer_name=r.customer_name,
                email=r.email,
                phone_number=r.phone_number,
                total_orders=r.total_orders,
                total_spent=float(r.total_spent or 0),
                average_ticket=float(r.average_ticket or 0),
                last_order_date=r.last_order_date,
                days_since_last_order=(datetime.now() - r.last_order_date).days,
                first_order_date=r.first_order_date
            )
            for r in results
        ]
    
    def get_delivery_performance(self, date_range: Optional[DateRangeFilter] = None,
                                filters: Optional[DimensionFilter] = None) -> List[DeliveryPerformanceItem]:
        """Get delivery performance by location"""
        avg_delivery = func.avg(Sale.delivery_seconds / 60.0)
        avg_production = func.avg(Sale.production_seconds / 60.0)
        
        query = self.db.query(
            DeliveryAddress.neighborhood,
            DeliveryAddress.city,
            func.count(Sale.id).label('total_deliveries'),
            avg_delivery.label('avg_delivery_time'),
            avg_production.label('avg_production_time'),
            (avg_delivery + avg_production).label('total_time')
        ).select_from(Sale)\
         .join(DeliveryAddress, Sale.id == DeliveryAddress.sale_id)
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(
            Sale.sale_status_desc == 'COMPLETED',
            Sale.delivery_seconds.isnot(None)
        )
        query = query.group_by(DeliveryAddress.neighborhood, DeliveryAddress.city)
        query = query.having(func.count(Sale.id) >= 5)  # Minimum 5 deliveries
        query = query.order_by((func.avg(Sale.delivery_seconds / 60.0) + func.avg(Sale.production_seconds / 60.0)).desc())
        
        results = query.all()
        
        return [
            DeliveryPerformanceItem(
                neighborhood=r.neighborhood,
                city=r.city,
                total_deliveries=r.total_deliveries or 0,
                avg_delivery_time_minutes=float(r.avg_delivery_time or 0),
                avg_production_time_minutes=float(r.avg_production_time or 0),
                total_delivery_time_minutes=float(r.total_time or 0)
            )
            for r in results
        ]
    
    def get_hourly_performance(self, date_range: Optional[DateRangeFilter] = None,
                              filters: Optional[DimensionFilter] = None,
                              day_of_week: Optional[int] = None) -> List[HourlyPerformanceItem]:
        """Get performance by hour and optionally day of week"""
        hour_extract = extract('hour', Sale.created_at)
        dow_extract = extract('dow', Sale.created_at)  # 0=Sunday, 6=Saturday
        
        query = self.db.query(
            hour_extract.label('hour'),
            dow_extract.label('day_of_week'),
            func.count(Sale.id).label('sales_count'),
            func.sum(Sale.total_amount).label('revenue'),
            func.avg(Sale.total_amount).label('average_ticket')
        )
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(Sale.sale_status_desc == 'COMPLETED')
        
        if day_of_week is not None:
            query = query.filter(dow_extract == day_of_week)
            query = query.group_by(hour_extract)
        else:
            query = query.group_by(hour_extract, dow_extract)
        
        query = query.order_by(hour_extract)
        
        results = query.all()
        
        day_names = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        
        return [
            HourlyPerformanceItem(
                hour=int(r.hour),
                day_of_week=int(r.day_of_week) if hasattr(r, 'day_of_week') and r.day_of_week is not None else None,
                day_name=day_names[int(r.day_of_week)] if hasattr(r, 'day_of_week') and r.day_of_week is not None else None,
                sales_count=r.sales_count or 0,
                revenue=float(r.revenue or 0),
                average_ticket=float(r.average_ticket or 0)
            )
            for r in results
        ]
    
    def get_product_margin_analysis(self, date_range: Optional[DateRangeFilter] = None,
                                   filters: Optional[DimensionFilter] = None,
                                   limit: int = 50) -> List[ProductMarginItem]:
        """Analyze product margins and customizations"""
        query = self.db.query(
            Product.id.label('product_id'),
            Product.name.label('product_name'),
            Category.name.label('category_name'),
            func.avg(ProductSale.base_price).label('avg_base_price'),
            func.avg(ProductSale.total_price).label('avg_total_price'),
            func.avg(ProductSale.total_price - ProductSale.base_price).label('avg_customization'),
            func.sum(ProductSale.total_price).label('total_revenue'),
            func.count(func.distinct(Sale.id)).label('order_count')
        ).select_from(ProductSale)\
         .join(Product, ProductSale.product_id == Product.id)\
         .join(Sale, ProductSale.sale_id == Sale.id)\
         .outerjoin(Category, Product.category_id == Category.id)
        
        query = self._apply_filters(query, date_range, filters)
        query = query.filter(Sale.sale_status_desc == 'COMPLETED')
        query = query.group_by(Product.id, Product.name, Category.name)
        query = query.order_by(func.sum(ProductSale.total_price).desc())
        query = query.limit(limit)
        
        results = query.all()
        
        return [
            ProductMarginItem(
                product_id=r.product_id,
                product_name=r.product_name,
                category_name=r.category_name,
                avg_base_price=float(r.avg_base_price or 0),
                avg_total_price=float(r.avg_total_price or 0),
                avg_customization_value=float(r.avg_customization or 0),
                total_revenue=float(r.total_revenue or 0),
                order_count=r.order_count or 0
            )
            for r in results
        ]
