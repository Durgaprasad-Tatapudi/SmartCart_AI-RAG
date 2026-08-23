from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import CartItemModel, ProductModel
from app.schemas.cart import CartResponse, CartItemResponse
from app.schemas.product import ProductResponse
from app.utils.pricing import calculate_cart_totals

class CartService:
    def get_cart(self, db: Session, session_id: str) -> CartResponse:
        """Retrieves and calculates server-verified cart state."""
        items = db.query(CartItemModel).filter(CartItemModel.session_id == session_id).all()
        
        item_responses = []
        calc_items = []
        
        for item in items:
            p = item.product
            if p:
                p_dict = p.to_dict()
                unit_price = float(p.price)
                total_price = unit_price * item.quantity
                
                item_responses.append(
                    CartItemResponse(
                        product_id=p.id,
                        quantity=item.quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        product=ProductResponse(**p_dict)
                    )
                )
                calc_items.append({
                    "price": unit_price,
                    "oldPrice": p_dict.get("oldPrice"),
                    "quantity": item.quantity
                })

        totals = calculate_cart_totals(calc_items)

        return CartResponse(
            session_id=session_id,
            items=item_responses,
            subtotal=totals["subtotal"],
            discount=totals["discount"],
            delivery=totals["delivery"],
            total=totals["total"],
            item_count=sum(i.quantity for i in items)
        )

    def add_to_cart(self, db: Session, session_id: str, product_id: str, quantity: int = 1) -> CartResponse:
        """Adds a product or increments quantity in the cart."""
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        existing = db.query(CartItemModel).filter(
            CartItemModel.session_id == session_id,
            CartItemModel.product_id == product_id
        ).first()

        if existing:
            existing.quantity += quantity
        else:
            new_item = CartItemModel(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity,
                price_at_addition=float(product.price)
            )
            db.add(new_item)

        db.commit()
        return self.get_cart(db, session_id)

    def update_cart_item(self, db: Session, session_id: str, product_id: str, quantity: int) -> CartResponse:
        """Updates item quantity or removes if <= 0."""
        item = db.query(CartItemModel).filter(
            CartItemModel.session_id == session_id,
            CartItemModel.product_id == product_id
        ).first()

        if item:
            if quantity <= 0:
                db.delete(item)
            else:
                item.quantity = quantity
            db.commit()

        return self.get_cart(db, session_id)

    def remove_from_cart(self, db: Session, session_id: str, product_id: str) -> CartResponse:
        """Removes a product from the cart."""
        item = db.query(CartItemModel).filter(
            CartItemModel.session_id == session_id,
            CartItemModel.product_id == product_id
        ).first()

        if item:
            db.delete(item)
            db.commit()

        return self.get_cart(db, session_id)

    def clear_cart(self, db: Session, session_id: str):
        """Clears all items in the cart."""
        db.query(CartItemModel).filter(CartItemModel.session_id == session_id).delete()
        db.commit()

cart_service = CartService()
