from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate
from app.services.cart_service import cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/{session_id}", response_model=CartResponse, summary="Get current cart")
def get_cart(session_id: str, db: Session = Depends(get_db)):
    return cart_service.get_cart(db, session_id)

@router.post("/{session_id}/items", response_model=CartResponse, summary="Add item to cart")
def add_item_to_cart(session_id: str, item: CartItemCreate, db: Session = Depends(get_db)):
    try:
        return cart_service.add_to_cart(db, session_id, item.product_id, item.quantity)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{session_id}/items/{product_id}", response_model=CartResponse, summary="Update item quantity")
def update_cart_item(session_id: str, product_id: str, item: CartItemUpdate, db: Session = Depends(get_db)):
    return cart_service.update_cart_item(db, session_id, product_id, item.quantity)

@router.delete("/{session_id}/items/{product_id}", response_model=CartResponse, summary="Remove item from cart")
def remove_from_cart(session_id: str, product_id: str, db: Session = Depends(get_db)):
    return cart_service.remove_from_cart(db, session_id, product_id)

@router.delete("/{session_id}", summary="Clear entire cart")
def clear_cart(session_id: str, db: Session = Depends(get_db)):
    cart_service.clear_cart(db, session_id)
    return {"message": "Cart cleared"}
