from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.schemas.product import ProductResponse

class ShippingAddress(BaseModel):
    full_name: str
    phone: str
    address_line: str
    city: str
    state: str
    pincode: str

class OrderCreate(BaseModel):
    session_id: str
    address: ShippingAddress
    payment_method: str = "UPI"  # "UPI" | "Card" | "COD"

class OrderItemResponse(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    total_price: float
    product: Optional[ProductResponse] = None

class OrderResponse(BaseModel):
    order_id: str
    id: str
    session_id: str
    created_at: str
    subtotal: float
    discount: float
    delivery: float
    total: float
    address: ShippingAddress
    payment_method: str
    status: str = "placed"
    demo: bool = True
    items: List[OrderItemResponse] = []
