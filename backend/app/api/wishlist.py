from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import WishlistItemModel, ProductModel
from app.schemas.product import ProductResponse

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.get("/{session_id}", response_model=List[ProductResponse], summary="Get wishlist products")
def get_wishlist(session_id: str, db: Session = Depends(get_db)):
    items = db.query(WishlistItemModel).filter(WishlistItemModel.session_id == session_id).all()
    products = []
    for item in items:
        if item.product:
            products.append(ProductResponse(**item.product.to_dict()))
    return products

@router.post("/{session_id}/{product_id}", summary="Toggle product in wishlist")
def toggle_wishlist(session_id: str, product_id: str, db: Session = Depends(get_db)):
    existing = db.query(WishlistItemModel).filter(
        WishlistItemModel.session_id == session_id,
        WishlistItemModel.product_id == product_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"wished": False, "product_id": product_id}
    else:
        prod = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not prod:
            raise HTTPException(status_code=404, detail="Product not found")
        new_w = WishlistItemModel(session_id=session_id, product_id=product_id)
        db.add(new_w)
        db.commit()
        return {"wished": True, "product_id": product_id}

@router.delete("/{session_id}/{product_id}", summary="Remove product from wishlist")
def remove_wishlist(session_id: str, product_id: str, db: Session = Depends(get_db)):
    existing = db.query(WishlistItemModel).filter(
        WishlistItemModel.session_id == session_id,
        WishlistItemModel.product_id == product_id
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
    return {"message": "Removed from wishlist", "product_id": product_id}
