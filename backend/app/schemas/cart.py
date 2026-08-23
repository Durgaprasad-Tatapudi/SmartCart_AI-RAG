from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.schemas.product import ProductResponse

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    total_price: float
    product: Optional[ProductResponse] = None

class CartResponse(BaseModel):
    session_id: str
    items: List[CartItemResponse] = []
    subtotal: float = 0.0
    discount: float = 0.0
    delivery: float = 0.0
    total: float = 0.0
    item_count: int = 0
