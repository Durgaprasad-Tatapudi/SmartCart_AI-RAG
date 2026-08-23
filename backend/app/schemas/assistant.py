from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.schemas.product import ProductResponse
from app.schemas.search import ShoppingIntent, RankedProduct

class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str

class AssistantChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = "default_session"
    session_id: Optional[str] = "default_session"
    history: List[ChatMessage] = []
    language: Optional[str] = None
    language_hint: Optional[str] = None

class FollowUpQuestion(BaseModel):
    question: str
    options: List[str] = []
    context_field: Optional[str] = None

class AssistantChatResponse(BaseModel):
    conversation_id: str
    message: str
    intent: Optional[ShoppingIntent] = None
    products: List[ProductResponse] = []
    exact_matches: List[ProductResponse] = []
    related_products: List[ProductResponse] = []
    has_exact_match: bool = True
    strict_constraints: List[str] = []
    ranked_products: List[RankedProduct] = []
    follow_up_question: Optional[FollowUpQuestion] = None
    suggestions: List[str] = []
    language: str = "english"
    demo: bool = True
    result_type: str = "EXACT_MATCH"  # EXACT_MATCH | NO_EXACT_BUT_NEARBY | NO_RELEVANT_PRODUCTS | INFORMATIONAL_QUERY
    budget_note: Optional[str] = None
    subscription_offer: Optional[Dict[str, Any]] = None  # {"show": true, "message": "...", "category": "...", "max_price": ...}


