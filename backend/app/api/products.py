from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import get_db
from app.schemas.product import ProductResponse, ProductListResponse
from app.services.product_service import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=ProductListResponse, summary="Explore and filter products")
def get_products(
    q: Optional[str] = Query(None, description="Search query keyword"),
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    min_price: Optional[float] = Query(None, description="Minimum price in INR"),
    max_price: Optional[float] = Query(None, description="Maximum price in INR"),
    min_rating: Optional[float] = Query(None, description="Minimum rating 1-5"),
    availability: Optional[str] = Query(None, description="in_stock / out_of_stock"),
    sort: Optional[str] = Query("best_match", description="best_match, price_asc, price_desc, rating_desc, discount_desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return product_service.get_products(
        db=db,
        q=q,
        category=category,
        subcategory=subcategory,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        availability=availability,
        sort=sort,
        page=page,
        limit=limit
    )

@router.get("/{product_id}", response_model=ProductResponse, summary="Get single product details")
def get_product(product_id: str, db: Session = Depends(get_db)):
    prod = product_service.get_product_by_id(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    return ProductResponse(**prod)

@router.get("/{product_id}/related", response_model=List[ProductResponse], summary="Get related products")
def get_related_products(product_id: str, limit: int = Query(4, ge=1, le=12), db: Session = Depends(get_db)):
    related = product_service.get_related_products(db, product_id, limit=limit)
    return [ProductResponse(**p) for p in related]
