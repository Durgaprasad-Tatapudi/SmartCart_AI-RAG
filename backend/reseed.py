from app.db.database import SessionLocal, engine, Base
from app.db.models import ProductModel, CategoryModel
from app.db.seed import seed_db
from app.services.vector_service import vector_service

db = SessionLocal()
try:
    print("Clearing old products...")
    db.query(ProductModel).delete()
    db.query(CategoryModel).delete()
    db.commit()

    print("Seeding new products...")
    seed_db(db)
    
    products = db.query(ProductModel).all()
    print(f"Total seeded products: {len(products)}")
    
    prod_dicts = [p.to_dict() for p in products]
    indexed = vector_service.index_products(prod_dicts)
    print(f"Total vector indexed: {indexed}")
finally:
    db.close()
