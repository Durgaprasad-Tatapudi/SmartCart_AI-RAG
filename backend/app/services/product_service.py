from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.db.models import ProductModel, CategoryModel
from app.schemas.product import ProductResponse, ProductListResponse, FiltersResponse

class ProductService:
    def get_products(
        self,
        db: Session,
        q: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        availability: Optional[str] = None,
        sort: Optional[str] = "best_match",
        page: int = 1,
        limit: int = 20
    ) -> ProductListResponse:
        """Queries and filters products from SQLite relational database."""
        query = db.query(ProductModel)

        # Keyword search across title, name, category, and search text
        if q:
            term = f"%{q.strip().lower()}%"
            query = query.filter(
                or_(
                    ProductModel.title.ilike(term),
                    ProductModel.name.ilike(term),
                    ProductModel.brand.ilike(term),
                    ProductModel.category.ilike(term),
                    ProductModel.subcategory.ilike(term),
                    ProductModel.search_text.ilike(term)
                )
            )

        if category and category.lower() != "all":
            query = query.filter(ProductModel.category.ilike(category))

        if subcategory:
            query = query.filter(ProductModel.subcategory.ilike(subcategory))

        if brand:
            query = query.filter(ProductModel.brand.ilike(brand))

        if min_price is not None:
            query = query.filter(ProductModel.price >= min_price)

        if max_price is not None:
            query = query.filter(ProductModel.price <= max_price)

        if min_rating is not None:
            query = query.filter(ProductModel.rating >= min_rating)

        if availability:
            query = query.filter(ProductModel.availability == availability)

        # Sorting
        if sort == "price_asc":
            query = query.order_by(asc(ProductModel.price))
        elif sort == "price_desc":
            query = query.order_by(desc(ProductModel.price))
        elif sort == "rating_desc":
            query = query.order_by(desc(ProductModel.rating), desc(ProductModel.reviews))
        elif sort == "discount_desc":
            query = query.order_by(desc(ProductModel.discount_percentage))
        else:  # best_match / default
            query = query.order_by(desc(ProductModel.rating), desc(ProductModel.reviews))

        total = query.count()
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()

        products = [ProductResponse(**item.to_dict()) for item in items]
        pages = (total + limit - 1) // limit if total > 0 else 1

        return ProductListResponse(
            products=products,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

    def get_product_by_id(self, db: Session, product_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves single product details."""
        item = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return item.to_dict() if item else None

    def get_related_products(self, db: Session, product_id: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Finds related products in same category/subcategory."""
        target = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not target:
            return []

        # Find other products in same subcategory or category
        query = db.query(ProductModel).filter(
            ProductModel.id != product_id,
            or_(
                ProductModel.subcategory == target.subcategory,
                ProductModel.category == target.category
            )
        ).order_by(desc(ProductModel.rating)).limit(limit)

        return [p.to_dict() for p in query.all()]

    def get_filters(self, db: Session) -> FiltersResponse:
        """Aggregates filter options available in catalogue."""
        products = db.query(ProductModel).all()
        categories = sorted(list(set(p.category for p in products if p.category)))
        subcategories = sorted(list(set(p.subcategory for p in products if p.subcategory)))
        brands = sorted(list(set(p.brand for p in products if p.brand)))
        prices = [p.price for p in products]
        min_p = min(prices) if prices else 0.0
        max_p = max(prices) if prices else 100000.0

        return FiltersResponse(
            categories=categories,
            subcategories=subcategories,
            brands=brands,
            minPrice=min_p,
            maxPrice=max_p,
            ratings=[4.5, 4.0, 3.5, 3.0],
            availability=["in_stock", "out_of_stock"]
        )

product_service = ProductService()
