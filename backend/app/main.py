from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.db.database import engine, Base, SessionLocal
from app.db.seed import seed_db
from app.db.models import ProductModel
from app.services.vector_service import vector_service
from app.services.embedding_service import embedding_service
from app.api import (
    health,
    products,
    categories,
    search,
    assistant,
    compare,
    cart,
    orders,
    wishlist,
    subscription
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    setup_logging()
    logger.info("Initializing SmartCart AI backend...")

    # 1. Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Relational database tables verified.")

    # 2. Seed database if empty
    db = SessionLocal()
    try:
        count = db.query(ProductModel).count()
        if count == 0:
            logger.info("Product catalogue empty. Seeding initial catalogue data...")
            seed_db(db)
        else:
            logger.info(f"Database contains {count} products.")
            
        # 3. Initialize Qdrant and verify vector indexing
        vector_service.connect()
        # Preload embeddings model in background
        embedding_service.initialize()
        
        # Check if Qdrant has vectors
        all_products = db.query(ProductModel).all()
        prod_dicts = [p.to_dict() for p in all_products]
        vector_service.index_products(prod_dicts)
    except Exception as e:
        logger.error(f"Startup initialization warning: {e}")
    finally:
        db.close()

    logger.info("SmartCart AI backend startup complete and ready.")
    yield
    logger.info("SmartCart AI backend shutting down.")

app = FastAPI(
    title="SmartCart AI API",
    description="Multilingual AI-Powered Shopping Assistant Backend with Qdrant Vector Search and OpenRouter LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again.",
                "details": str(exc) if settings.APP_ENV == "development" else None
            }
        }
    )

# Mount API Routers under /api/v1
api_prefix = settings.API_V1_STR
app.include_router(health.router, prefix=api_prefix)
app.include_router(products.router, prefix=api_prefix)
app.include_router(categories.router, prefix=api_prefix)
app.include_router(search.router, prefix=api_prefix)
app.include_router(assistant.router, prefix=api_prefix)
app.include_router(compare.router, prefix=api_prefix)
app.include_router(cart.router, prefix=api_prefix)
app.include_router(orders.router, prefix=api_prefix)
app.include_router(wishlist.router, prefix=api_prefix)
app.include_router(subscription.router, prefix=api_prefix)

@app.get("/", summary="Root redirect to Docs")
def root():
    return {
        "message": "SmartCart AI Backend is running.",
        "docs": "/docs",
        "health": f"{api_prefix}/health"
    }
