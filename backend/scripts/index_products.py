import sys
import os

# Add backend directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import SessionLocal
from app.db.models import ProductModel
from app.services.vector_service import vector_service
from app.core.logging import setup_logging, logger

def main():
    setup_logging()
    logger.info("Connecting to Qdrant vector database...")
    vector_service.connect()
    
    db = SessionLocal()
    try:
        products = db.query(ProductModel).all()
        prod_dicts = [p.to_dict() for p in products]
        logger.info(f"Loaded {len(prod_dicts)} products from database.")
        
        indexed_count = vector_service.index_products(prod_dicts)
        print(f"\n==========================================")
        print(f"Products loaded:     {len(prod_dicts)}")
        print(f"Vectors indexed:     {indexed_count}")
        print(f"Qdrant Collection:   {vector_service.collection_name}")
        print(f"Vector indexing complete!")
        print(f"==========================================\n")
    finally:
        db.close()

if __name__ == "__main__":
    main()
