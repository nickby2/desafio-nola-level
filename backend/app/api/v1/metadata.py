"""
Metadata API endpoints for dimensions (stores, channels, categories, etc.)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Store, Channel, Category, Product
from app.schemas.analytics import (
    MetadataResponse, StoreInfo, ChannelInfo, 
    CategoryInfo, ProductInfo
)

router = APIRouter()


@router.get("/metadata", response_model=MetadataResponse)
def get_metadata(db: Session = Depends(get_db)):
    """
    Get all metadata for filters
    
    Returns available stores, channels, and categories for use in filters.
    """
    # Get stores
    stores_query = db.query(Store).filter(Store.is_active == True).all()
    stores = [
        StoreInfo(
            id=s.id,
            name=s.name,
            city=s.city,
            state=s.state,
            is_active=s.is_active
        )
        for s in stores_query
    ]
    
    # Get channels
    channels_query = db.query(Channel).all()
    channels = [
        ChannelInfo(
            id=c.id,
            name=c.name,
            type=c.type,
            description=c.description
        )
        for c in channels_query
    ]
    
    # Get categories
    categories_query = db.query(Category).filter(Category.deleted_at.is_(None)).all()
    categories = [
        CategoryInfo(
            id=c.id,
            name=c.name,
            type=c.type
        )
        for c in categories_query
    ]
    
    return MetadataResponse(
        stores=stores,
        channels=channels,
        categories=categories
    )


@router.get("/stores", response_model=List[StoreInfo])
def get_stores(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all stores"""
    query = db.query(Store)
    if active_only:
        query = query.filter(Store.is_active == True)
    
    stores = query.all()
    return [
        StoreInfo(
            id=s.id,
            name=s.name,
            city=s.city,
            state=s.state,
            is_active=s.is_active
        )
        for s in stores
    ]


@router.get("/channels", response_model=List[ChannelInfo])
def get_channels(db: Session = Depends(get_db)):
    """Get all channels"""
    channels = db.query(Channel).all()
    return [
        ChannelInfo(
            id=c.id,
            name=c.name,
            type=c.type,
            description=c.description
        )
        for c in channels
    ]


@router.get("/categories", response_model=List[CategoryInfo])
def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).filter(Category.deleted_at.is_(None)).all()
    return [
        CategoryInfo(
            id=c.id,
            name=c.name,
            type=c.type
        )
        for c in categories
    ]


@router.get("/products", response_model=List[ProductInfo])
def get_products(
    category_id: int = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get products with optional category filter"""
    query = db.query(Product).filter(Product.deleted_at.is_(None))
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    query = query.limit(limit)
    products = query.all()
    
    return [
        ProductInfo(
            id=p.id,
            name=p.name,
            category_id=p.category_id
        )
        for p in products
    ]
