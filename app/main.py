from fastapi import FastAPI
from .db import connect, disconnect
from .routers import analytics

app = FastAPI(title="Restaurant Analytics — Backend")


@app.on_event("startup")
async def startup():
    await connect()


@app.on_event("shutdown")
async def shutdown():
    await disconnect()


app.include_router(analytics.router)


@app.get("/")
async def root():
    return {"ok": True, "service": "restaurant-analytics-backend"}
