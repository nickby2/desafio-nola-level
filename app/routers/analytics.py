from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ..db import database
from .. import schemas
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/health", response_model=schemas.HealthResponse)
async def health():
    # simple DB connectivity check
    try:
        await database.connect()
        await database.disconnect()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-products", response_model=List[schemas.TopProductItem])
async def top_products(
    channel: Optional[str] = Query(None, description="Channel name, e.g. iFood"),
    dow: Optional[int] = Query(None, description="day of week (0=Sun .. 6=Sat)"),
    hour_start: Optional[int] = Query(None),
    hour_end: Optional[int] = Query(None),
    limit: int = Query(10),
):
    """Top products filtered by channel, day-of-week and hour range."""
    params = {}
    where_clauses = ["s.sale_status_desc ILIKE 'completed'%s"]
    # We'll build query carefully and parameterize inputs
    sql = """
    SELECT p.id AS product_id, p.name AS product_name, SUM(ps.quantity) AS quantity
    FROM sales s
    JOIN product_sales ps ON ps.sale_id = s.id
    JOIN products p ON p.id = ps.product_id
    JOIN channels c ON c.id = s.channel_id
    WHERE s.sale_status_desc ILIKE 'completed'
    """

    if channel:
        sql += " AND c.name ILIKE :channel"
        params["channel"] = f"%{channel}%"
    if dow is not None:
        sql += " AND EXTRACT(DOW FROM s.created_at) = :dow"
        params["dow"] = dow
    if hour_start is not None and hour_end is not None:
        sql += " AND EXTRACT(HOUR FROM s.created_at) BETWEEN :hs AND :he"
        params["hs"] = hour_start
        params["he"] = hour_end

    sql += " GROUP BY p.id, p.name ORDER BY quantity DESC LIMIT :limit"
    params["limit"] = limit

    rows = await database.fetch_all(query=sql, values=params)
    return [dict(r) for r in rows]


@router.get("/ticket-trend")
async def ticket_trend(
    group_by: str = Query("channel", regex="^(channel|store)$"),
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    """Return average ticket grouped by channel or store for periods (monthly)."""
    params = {}
    sql = """
    SELECT
        {gb}_id as group_id,
        DATE_TRUNC('day', s.created_at) AS period_start,
        AVG(s.total_amount) as avg_ticket
    FROM sales s
    WHERE s.sale_status_desc ILIKE 'completed'
    """.replace("{gb}", "channel" if group_by == "channel" else "store")

    if start:
        sql += " AND s.created_at >= :start"
        params["start"] = start
    if end:
        sql += " AND s.created_at <= :end"
        params["end"] = end

    sql += f" GROUP BY { 'channel_id' if group_by=='channel' else 'store_id' }, DATE_TRUNC('day', s.created_at) ORDER BY period_start"

    rows = await database.fetch_all(query=sql, values=params)
    return [dict(r) for r in rows]


@router.get("/delivery-performance")
async def delivery_performance(start: Optional[datetime] = None, end: Optional[datetime] = None):
    params = {}
    sql = """
    SELECT
        EXTRACT(DOW FROM s.created_at) AS day_of_week,
        EXTRACT(HOUR FROM s.created_at) AS hour,
        AVG(s.delivery_seconds) AS avg_delivery_seconds
    FROM sales s
    WHERE s.sale_status_desc ILIKE 'completed' AND s.delivery_seconds IS NOT NULL
    """
    if start:
        sql += " AND s.created_at >= :start"
        params["start"] = start
    if end:
        sql += " AND s.created_at <= :end"
        params["end"] = end
    sql += " GROUP BY day_of_week, hour ORDER BY day_of_week, hour"

    rows = await database.fetch_all(query=sql, values=params)
    return [dict(r) for r in rows]


@router.get("/churned-customers", response_model=List[schemas.ChurnedCustomer])
async def churned_customers(min_orders: int = 3, days: int = 30):
    sql = """
    SELECT c.id as customer_id, c.customer_name, MAX(s.created_at) as last_order_at, COUNT(s.id) as orders_count
    FROM customers c
    JOIN sales s ON s.customer_id = c.id AND s.sale_status_desc ILIKE 'completed'
    GROUP BY c.id, c.customer_name
    HAVING COUNT(s.id) >= :min_orders AND MAX(s.created_at) < (NOW() - (:days || ' days')::interval)
    ORDER BY last_order_at DESC
    """
    rows = await database.fetch_all(query=sql, values={"min_orders": min_orders, "days": days})
    return [dict(r) for r in rows]


@router.get("/low-margin-products")
async def low_margin_products(limit: int = 20):
    # NOTE: schema doesn't include product cost; this endpoint expects a `cost` column
    sql = """
    SELECT p.id as product_id, p.name as product_name,
        SUM(ps.total_price) as revenue,
        SUM(ps.quantity * COALESCE(p.cost,0)) as est_cost,
        (SUM(ps.total_price) - SUM(ps.quantity * COALESCE(p.cost,0))) as gross_profit
    FROM product_sales ps
    JOIN products p ON p.id = ps.product_id
    JOIN sales s ON s.id = ps.sale_id AND s.sale_status_desc ILIKE 'completed'
    GROUP BY p.id, p.name
    ORDER BY gross_profit ASC
    LIMIT :limit
    """
    rows = await database.fetch_all(query=sql, values={"limit": limit})
    return [dict(r) for r in rows]
