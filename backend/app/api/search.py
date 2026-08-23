from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models import SearchHistoryModel
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_service import search_service
from app.core.security import sanitize_query

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("", response_model=SearchResponse, summary="Natural language AI search")
async def search_products(request: SearchRequest, db: Session = Depends(get_db)):
    request.query = sanitize_query(request.query)
    return await search_service.search(db, request)

@router.post("/semantic", response_model=SearchResponse, summary="Semantic vector search")
async def semantic_search(request: SearchRequest, db: Session = Depends(get_db)):
    request.query = sanitize_query(request.query)
    return await search_service.search(db, request)

@router.get("/history/{session_id}", summary="Get recent searches for session")
def get_search_history(session_id: str, db: Session = Depends(get_db)):
    history = db.query(SearchHistoryModel).filter(
        SearchHistoryModel.session_id == session_id
    ).order_by(SearchHistoryModel.created_at.desc()).limit(10).all()
    return [{"query": h.query, "created_at": h.created_at.isoformat()} for h in history]

@router.delete("/history/{session_id}", summary="Clear search history")
def clear_search_history(session_id: str, db: Session = Depends(get_db)):
    db.query(SearchHistoryModel).filter(SearchHistoryModel.session_id == session_id).delete()
    db.commit()
    return {"message": "Search history cleared"}
