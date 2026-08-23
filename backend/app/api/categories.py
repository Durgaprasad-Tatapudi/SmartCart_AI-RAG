from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import CategoryModel
from app.schemas.product import CategoryResponse, FiltersResponse
from app.services.product_service import product_service

router = APIRouter(tags=["Categories"])

@router.get("/categories", response_model=List[CategoryResponse], summary="List all product categories")
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(CategoryModel).all()
    return [CategoryResponse(**c.to_dict()) for c in cats]

@router.get("/filters", response_model=FiltersResponse, summary="Get dynamic filter facets")
def get_filters(db: Session = Depends(get_db)):
    return product_service.get_filters(db)
