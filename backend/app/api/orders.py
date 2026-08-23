from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import order_service

router = APIRouter(tags=["Orders"])

@router.post("/orders", response_model=OrderResponse, summary="Place demo order")
def place_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    try:
        return order_service.create_order(db, order_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{session_id}", response_model=List[OrderResponse], summary="List orders for session")
def get_orders(session_id: str, db: Session = Depends(get_db)):
    return order_service.get_orders_by_session(db, session_id)

@router.get("/orders/{session_id}/{order_id}", response_model=OrderResponse, summary="Get order details")
def get_order(session_id: str, order_id: str, db: Session = Depends(get_db)):
    order = order_service.get_order_by_id(db, session_id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order
