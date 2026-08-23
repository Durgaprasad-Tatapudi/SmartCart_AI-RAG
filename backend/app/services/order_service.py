import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import OrderModel, OrderItemModel, CartItemModel, ProductModel
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse
from app.schemas.product import ProductResponse
from app.services.cart_service import cart_service

class OrderService:
    def create_order(self, db: Session, order_in: OrderCreate) -> OrderResponse:
        """
        Creates a demo order from current session's cart, validates totals,
        creates snapshot items, clears the cart, and returns the order.
        """
        cart = cart_service.get_cart(db, order_in.session_id)
        if not cart.items:
            raise ValueError("Cannot checkout with an empty cart.")

        order_id = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        new_order = OrderModel(
            id=order_id,
            session_id=order_in.session_id,
            created_at=datetime.utcnow(),
            subtotal=cart.subtotal,
            discount=cart.discount,
            delivery=cart.delivery,
            total=cart.total,
            address_json=json.dumps(order_in.address.model_dump()),
            payment_method=order_in.payment_method,
            status="placed",
            demo=True
        )
        db.add(new_order)
        db.flush()

        order_item_responses = []
        for c_item in cart.items:
            order_item = OrderItemModel(
                order_id=order_id,
                product_id=c_item.product_id,
                quantity=c_item.quantity,
                unit_price=c_item.unit_price,
                total_price=c_item.total_price,
                product_snapshot_json=json.dumps(c_item.product.model_dump() if c_item.product else {})
            )
            db.add(order_item)
            order_item_responses.append(
                OrderItemResponse(
                    product_id=c_item.product_id,
                    quantity=c_item.quantity,
                    unit_price=c_item.unit_price,
                    total_price=c_item.total_price,
                    product=c_item.product
                )
            )

        # Clear cart
        cart_service.clear_cart(db, order_in.session_id)
        db.commit()

        return OrderResponse(
            order_id=order_id,
            id=order_id,
            session_id=order_in.session_id,
            created_at=new_order.created_at.isoformat(),
            subtotal=cart.subtotal,
            discount=cart.discount,
            delivery=cart.delivery,
            total=cart.total,
            address=order_in.address,
            payment_method=order_in.payment_method,
            status="placed",
            demo=True,
            items=order_item_responses
        )

    def get_orders_by_session(self, db: Session, session_id: str) -> List[OrderResponse]:
        """Retrieves all orders placed in this browser session."""
        orders = db.query(OrderModel).filter(OrderModel.session_id == session_id).order_by(OrderModel.created_at.desc()).all()
        return [OrderResponse(**o.to_dict()) for o in orders]

    def get_order_by_id(self, db: Session, session_id: str, order_id: str) -> Optional[OrderResponse]:
        """Retrieves a specific order."""
        order = db.query(OrderModel).filter(
            OrderModel.session_id == session_id,
            OrderModel.id == order_id
        ).first()
        return OrderResponse(**order.to_dict()) if order else None

order_service = OrderService()
