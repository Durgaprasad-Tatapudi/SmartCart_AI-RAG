from pydantic import BaseModel
from typing import Optional

class SubscriptionRequest(BaseModel):
    email: Optional[str] = None
    session_id: Optional[str] = None
    category: str
    max_price: Optional[float] = None
    use_case: Optional[str] = None
    language: str = "english"

class SubscriptionResponse(BaseModel):
    success: bool
    message: str
    subscription_id: Optional[str] = None
