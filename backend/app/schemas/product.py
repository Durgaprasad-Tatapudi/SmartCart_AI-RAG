from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ProductBase(BaseModel):
    id: str
    sku: Optional[str] = None
    title: str
    name: str
    brand: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    price: float
    oldPrice: Optional[float] = None
    originalPrice: Optional[float] = None
    discountPercentage: Optional[int] = 0
    rating: float = 4.5
    reviews: int = 0
    reviewCount: int = 0
    image: str
    images: Optional[List[str]] = None
    badge: Optional[str] = None
    specs: List[str] = []
    description: Optional[str] = None
    features: Optional[List[str]] = []
    specifications: Optional[Dict[str, Any]] = {}
    tags: Optional[List[str]] = []
    availability: Optional[str] = "in_stock"
    stock: Optional[int] = 50
    deliveryInfo: Optional[str] = "Free 2-day delivery"
    # AI recommendation fields
    why_recommended: Optional[str] = None
    budget_status: Optional[str] = None  # "within_budget" | "above_budget"
    budget_difference: Optional[float] = None  # positive = above budget by this amount

class ProductResponse(ProductBase):
    pass

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int = 1
    limit: int = 20
    pages: int = 1

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    subcategories: List[str] = []

class FiltersResponse(BaseModel):
    categories: List[str]
    subcategories: List[str]
    brands: List[str]
    minPrice: float
    maxPrice: float
    ratings: List[float]
    availability: List[str]
