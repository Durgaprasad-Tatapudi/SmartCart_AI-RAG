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
    logger.info("Rebuilding Qdrant vector index...")
    vector_service.connect()
    
    try:
        if vector_service.client:
            logger.info(f"Deleting existing collection '{vector_service.collection_name}'...")
            vector_service.client.delete_collection(vector_service.collection_name)
    except Exception as e:
        logger.warning(f"Could not delete collection ({e}), recreating...")

    vector_service.ensure_collection()
    
    db = SessionLocal()
    try:
        products = db.query(ProductModel).all()
        prod_dicts = [p.to_dict() for p in products]
        indexed_count = vector_service.index_products(prod_dicts)
        print(f"Rebuild completed: {indexed_count} product vectors re-indexed.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
