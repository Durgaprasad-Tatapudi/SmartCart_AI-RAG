import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # App
    APP_NAME: str = "SmartCart AI Backend"
    APP_ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    # SQLite Database
    DATABASE_URL: str = "sqlite:///./smartcart.db"
    
    # Qdrant Vector DB
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    QDRANT_COLLECTION: str = "smartcart_products"
    
    # OpenRouter LLM
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct:free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Embeddings
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIM: int = 384

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
