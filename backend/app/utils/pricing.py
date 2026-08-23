from typing import List, Dict, Any

def calculate_discount_percentage(original_price: float, price: float) -> int:
    if not original_price or original_price <= price:
        return 0
    return int(round((1 - price / original_price) * 100))

def calculate_cart_totals(items: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculates subtotal, discount, delivery fee, and grand total for a list of cart items.
    """
    subtotal = 0.0
    total_savings = 0.0
    
    for item in items:
        qty = item.get("quantity", 1)
        price = item.get("price", 0.0)
        old_price = item.get("oldPrice") or item.get("originalPrice") or price
        
        subtotal += price * qty
        if old_price > price:
            total_savings += (old_price - price) * qty
            
    # Free delivery on orders over ₹499, else ₹40
    delivery = 0.0 if subtotal >= 499 or subtotal == 0 else 40.0
    grand_total = subtotal + delivery

    return {
        "subtotal": round(subtotal, 2),
        "discount": round(total_savings, 2),
        "delivery": round(delivery, 2),
        "total": round(grand_total, 2)
    }
