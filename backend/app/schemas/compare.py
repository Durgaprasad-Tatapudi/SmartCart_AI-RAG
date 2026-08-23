from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.schemas.product import ProductResponse

class CompareRequest(BaseModel):
    product_ids: List[str]

class CompareExplainRequest(BaseModel):
    product_ids: List[str]
    query: Optional[str] = "Which product is better for my needs?"
    language: Optional[str] = "english"

class ComparisonSummary(BaseModel):
    price: Dict[str, Any] = {}
    rating: Dict[str, Any] = {}
    specifications: Dict[str, Any] = {}
    highlights: List[str] = []

class CompareResponse(BaseModel):
    products: List[ProductResponse]
    comparison: ComparisonSummary
    explanation: Optional[str] = None
