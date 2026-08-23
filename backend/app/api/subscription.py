from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import SubscriptionModel
from app.schemas.subscription import SubscriptionRequest, SubscriptionResponse
from app.core.logging import logger

router = APIRouter(prefix="/subscribe", tags=["Subscription"])

@router.post("", response_model=SubscriptionResponse, summary="Subscribe to product availability alerts")
def create_subscription(request: SubscriptionRequest, db: Session = Depends(get_db)):
    """Creates a subscription alert for when products matching criteria become available."""
    try:
        sub = SubscriptionModel(
            session_id=request.session_id or "anonymous",
            email=request.email,
            category=request.category,
            max_price=request.max_price,
            use_case=request.use_case,
            language=request.language,
            active=True
        )
        db.add(sub)
        db.commit()
        db.refresh(sub)

        is_telugu = request.language.lower() in ["te", "telugu"]
        if is_telugu:
            price_str = f"₹{request.max_price:,.0f} లోపు " if request.max_price else ""
            msg = f"{price_str}{request.category} అందుబాటులోకి వచ్చినప్పుడు మీకు తెలియజేస్తాము. మీ alert విజయవంతంగా సెట్ చేయబడింది!"
        else:
            price_str = f"under ₹{request.max_price:,.0f} " if request.max_price else ""
            msg = f"You'll be notified when {price_str}{request.category} products become available. Your alert has been set successfully!"

        return SubscriptionResponse(
            success=True,
            message=msg,
            subscription_id=str(sub.id)
        )
    except Exception as e:
        logger.error(f"Subscription creation failed: {e}")
        return SubscriptionResponse(
            success=False,
            message="Failed to create subscription. Please try again."
        )
