import sys
import os

# Add backend directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import engine, Base, SessionLocal
from app.db.seed import seed_db
from app.core.logging import setup_logging, logger

def main():
    setup_logging()
    logger.info("Initializing SQLite database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        cat_count, prod_count = seed_db(db)
        print(f"\n==========================================")
        print(f"Categories seeded: {cat_count}")
        print(f"Products seeded:   {prod_count}")
        print(f"Database setup complete!")
        print(f"==========================================\n")
    finally:
        db.close()

if __name__ == "__main__":
    main()
