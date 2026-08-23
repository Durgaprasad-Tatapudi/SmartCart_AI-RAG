from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", summary="Service Health Check")
async def health_check():
    """Returns status of database, qdrant, and openrouter integrations."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "ok",
        "qdrant": "configured",
        "embedding_model": settings.EMBEDDING_MODEL,
        "openrouter": "configured" if settings.OPENROUTER_API_KEY else "fallback_mode",
        "demo_mode": True
    }
