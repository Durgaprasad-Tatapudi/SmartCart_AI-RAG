from datetime import datetime
import json
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    category = Column(String, index=True)
    subcategory = Column(String, index=True)
    price = Column(Float, index=True)
    old_price = Column(Float, nullable=True)
    discount_percentage = Column(Integer, default=0)
    rating = Column(Float, default=4.5)
    reviews = Column(Integer, default=0)
    image = Column(String)
    images_json = Column(Text, default="[]")
    badge = Column(String, nullable=True)
    specs_json = Column(Text, default="[]")
    description = Column(Text)
    features_json = Column(Text, default="[]")
    specifications_json = Column(Text, default="{}")
    tags_json = Column(Text, default="[]")
    availability = Column(String, default="in_stock")
    stock = Column(Integer, default=50)
    delivery_info = Column(String, default="Free 2-day delivery")
    search_text = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "title": self.title,
            "name": self.name or self.title,
            "brand": self.brand,
            "category": self.category,
            "subcategory": self.subcategory,
            "price": self.price,
            "oldPrice": self.old_price,
            "originalPrice": self.old_price or self.price,
            "discountPercentage": self.discount_percentage,
            "rating": self.rating,
            "reviews": self.reviews,
            "reviewCount": self.reviews,
            "image": self.image,
            "images": json.loads(self.images_json) if self.images_json else [self.image],
            "badge": self.badge,
            "specs": json.loads(self.specs_json) if self.specs_json else [],
            "description": self.description,
            "features": json.loads(self.features_json) if self.features_json else [],
            "specifications": json.loads(self.specifications_json) if self.specifications_json else {},
            "tags": json.loads(self.tags_json) if self.tags_json else [],
            "availability": self.availability,
            "stock": self.stock,
            "deliveryInfo": self.delivery_info,
        }

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    subcategories_json = Column(Text, default="[]")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subcategories": json.loads(self.subcategories_json) if self.subcategories_json else []
        }

class CartItemModel(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price_at_addition = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("ProductModel")

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float)
    discount = Column(Float, default=0.0)
    delivery = Column(Float, default=0.0)
    total = Column(Float)
    address_json = Column(Text)
    payment_method = Column(String, default="UPI")
    status = Column(String, default="placed")
    demo = Column(Boolean, default=True)

    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "order_id": self.id,
            "id": self.id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat() if self.created_at else datetime.utcnow().isoformat(),
            "subtotal": self.subtotal,
            "discount": self.discount,
            "delivery": self.delivery,
            "total": self.total,
            "address": json.loads(self.address_json) if self.address_json else {},
            "payment_method": self.payment_method,
            "status": self.status,
            "demo": self.demo,
            "items": [item.to_dict() for item in self.items]
        }

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float)
    total_price = Column(Float)
    product_snapshot_json = Column(Text)

    order = relationship("OrderModel", back_populates="items")

    def to_dict(self):
        snapshot = json.loads(self.product_snapshot_json) if self.product_snapshot_json else {}
        return {
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "product": snapshot
        }

class WishlistItemModel(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    product_id = Column(String, ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("ProductModel")

class SearchHistoryModel(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    query = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    email = Column(String, nullable=True)
    category = Column(String, index=True)
    max_price = Column(Float, nullable=True)
    use_case = Column(String, nullable=True)
    language = Column(String, default="english")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

