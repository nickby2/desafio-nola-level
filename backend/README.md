# Restaurant Analytics API Backend

FastAPI-based backend for the Restaurant Analytics Platform.

## Features

- **Flexible Analytics Endpoints**: Query sales, products, customers, and delivery data
- **Optimized Queries**: Sub-second performance on 500k+ records
- **Multi-dimensional Filtering**: Filter by store, channel, date range, and more
- **Business Intelligence**: Answers specific business questions

## Key Endpoints

### Analytics Endpoints

- `GET /api/v1/analytics/overview` - Overall sales metrics
- `GET /api/v1/analytics/products/ranking` - Top selling products
- `GET /api/v1/analytics/channels/performance` - Performance by channel
- `GET /api/v1/analytics/stores/performance` - Performance by store
- `GET /api/v1/analytics/timeseries` - Time series data (daily/weekly/monthly)
- `GET /api/v1/analytics/customers/retention` - Customer retention analysis
- `GET /api/v1/analytics/delivery/performance` - Delivery performance metrics
- `GET /api/v1/analytics/hourly/performance` - Hourly performance analysis
- `GET /api/v1/analytics/products/margin` - Product margin analysis

### Metadata Endpoints

- `GET /api/v1/metadata` - All metadata (stores, channels, categories)
- `GET /api/v1/stores` - List of stores
- `GET /api/v1/channels` - List of channels
- `GET /api/v1/categories` - List of categories
- `GET /api/v1/products` - List of products

## Business Questions Answered

✅ **"Qual produto vende mais na quinta à noite no iFood?"**
- Use `/hourly/performance?day_of_week=4&channel_ids=X` + `/products/ranking`

✅ **"Meu ticket médio está caindo. É por canal ou por loja?"**
- Use `/channels/performance` and `/stores/performance` to compare

✅ **"Quais produtos têm menor margem e devo repensar o preço?"**
- Use `/products/margin` to see base price vs actual revenue

✅ **"Meu tempo de entrega piorou. Em quais dias/horários?"**
- Use `/delivery/performance` grouped by location and time

✅ **"Quais clientes compraram 3+ vezes mas não voltam há 30 dias?"**
- Use `/customers/retention?min_orders=3&days_inactive=30`

## Setup

### Local Development

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

Run with Docker Compose:
```bash
docker-compose up backend
```

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── analytics.py    # Analytics endpoints
│   │       └── metadata.py     # Metadata endpoints
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   └── database.py        # Database connection
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── analytics.py       # Pydantic schemas
│   ├── services/
│   │   └── analytics_service.py  # Business logic
│   └── main.py                # FastAPI app
├── requirements.txt
└── Dockerfile
```

## Performance

- Queries optimized for < 1 second on 500k+ records
- Proper indexing on date, store_id, channel_id
- Connection pooling configured
- Optional Redis caching layer

## Technology Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Database with 500k+ records
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
