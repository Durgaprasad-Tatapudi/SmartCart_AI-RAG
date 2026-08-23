from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Union
from app.schemas.product import ProductResponse

class ShoppingIntent(BaseModel):
    query: str
    normalized_query: Optional[str] = None
    language: str = "english"
    category: Optional[str] = None
    subcategory: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    brands: List[str] = []
    use_case: List[str] = []
    features: List[str] = []
    specifications: Dict[str, Any] = {}
    ram: Optional[str] = None
    storage: Optional[str] = None
    display: Optional[str] = None
    strict_constraints: List[str] = []
    is_strict: bool = False
    minimum_rating: Optional[float] = None
    availability: Optional[str] = None
    sort_preference: Optional[str] = None
    comparison_intent: bool = False
    cheaper_request: bool = False
    similar_request: bool = False

    @field_validator("use_case", "brands", "features", mode="before")
    @classmethod
    def ensure_list(cls, v):
        if isinstance(v, str):
            return [v] if v.strip() else []
        return v or []

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    session_id: Optional[str] = None

class RankedProduct(BaseModel):
    product: ProductResponse
    match_score: float = 1.0
    match_reasons: List[str] = []

class SearchResponse(BaseModel):
    query: str
    language: str = "english"
    intent: Optional[ShoppingIntent] = None
    results: List[RankedProduct] = []
    products: List[ProductResponse] = []
    total: int = 0
    explanation: Optional[str] = None
    filters_applied: Dict[str, Any] = {}
    fallback_search: bool = False
    result_type: str = "EXACT_MATCH"
    budget_note: Optional[str] = None

