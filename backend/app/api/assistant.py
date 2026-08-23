from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.assistant import AssistantChatRequest, AssistantChatResponse
from app.schemas.search import SearchRequest
from app.services.search_service import search_service
from app.services.llm_service import llm_service
from app.core.security import sanitize_query

router = APIRouter(prefix="/assistant", tags=["Assistant"])

@router.post("/chat", response_model=AssistantChatResponse, summary="Multilingual AI Shopping Assistant Chat")
async def chat_with_assistant(request: AssistantChatRequest, db: Session = Depends(get_db)):
    clean_msg = sanitize_query(request.message)
    
    # 1. Execute search pipeline to retrieve real candidates
    search_req = SearchRequest(
        query=clean_msg,
        limit=5,
        session_id=request.session_id
    )
    search_res = await search_service.search(db, search_req)
    
    # Honor language preference from UI selector if provided
    active_lang = search_res.language
    if request.language:
        if request.language.lower() in ["te", "telugu"]:
            active_lang = "telugu"
        elif request.language.lower() in ["en", "english"]:
            active_lang = "english"
            
    if search_res.intent:
        search_res.intent.language = active_lang

    # 2. Convert candidate products to dicts for LLM grounding
    candidate_dicts = [p.model_dump() for p in search_res.products]
    
    # 3. Generate grounded multilingual response
    reply_text, follow_up, suggestions = await llm_service.generate_assistant_response(
        query=clean_msg,
        intent=search_res.intent,
        products=candidate_dicts,
        history=request.history,
        language=active_lang,
        result_type=search_res.result_type
    )

    # 4. Construct subscription offer if exact constraint could not be met or category is unavailable
    subscription_offer = None
    if search_res.result_type in ["NO_EXACT_BUT_NEARBY", "NO_RELEVANT_PRODUCTS"]:
        is_telugu = active_lang.lower() in ["te", "telugu"]
        cat_name = search_res.intent.subcategory or search_res.intent.category or ("ఉత్పత్తులు" if is_telugu else "products")
        max_p = search_res.intent.max_price
        
        if is_telugu:
            if max_p:
                sub_msg = f"మీకు ₹{max_p:,.0f} limit లోపు {cat_name} మాత్రమే కావాలంటే, ఆ budget లో కొత్త options వచ్చినప్పుడు మీకు తెలియజేయడానికి alert set చేసుకోండి."
            else:
                sub_msg = f"{cat_name} మా catalogue లోకి వచ్చినప్పుడు మీకు తెలియజేయడానికి alert set చేసుకోండి."
        else:
            if max_p:
                sub_msg = f"If you only want {cat_name} under ₹{max_p:,.0f}, set an alert and we'll notify you as soon as matching products arrive."
            else:
                sub_msg = f"Get notified as soon as {cat_name} become available in our catalogue."
                
        subscription_offer = {
            "show": True,
            "message": sub_msg,
            "category": search_res.intent.category or search_res.intent.subcategory or "General",
            "max_price": max_p,
            "ram": search_res.intent.ram,
            "storage": search_res.intent.storage,
            "display": search_res.intent.display,
            "language": active_lang
        }

    exact_matches = []
    related_products = []
    has_exact_match = (search_res.result_type == "EXACT_MATCH")
    if search_res.result_type == "EXACT_MATCH":
        exact_matches = search_res.products
    elif search_res.result_type == "NO_EXACT_BUT_NEARBY":
        related_products = search_res.products

    strict_constraints = search_res.intent.strict_constraints if search_res.intent else []

    return AssistantChatResponse(
        conversation_id=request.conversation_id or "default_session",
        message=reply_text,
        intent=search_res.intent,
        products=search_res.products,
        exact_matches=exact_matches,
        related_products=related_products,
        has_exact_match=has_exact_match,
        strict_constraints=strict_constraints,
        ranked_products=search_res.results,
        follow_up_question=follow_up,
        suggestions=suggestions,
        language=active_lang,
        demo=True,
        result_type=search_res.result_type,
        budget_note=search_res.budget_note,
        subscription_offer=subscription_offer
    )

