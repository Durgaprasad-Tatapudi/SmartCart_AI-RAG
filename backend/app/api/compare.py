from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ProductModel
from app.schemas.compare import CompareRequest, CompareExplainRequest, CompareResponse, ComparisonSummary
from app.schemas.product import ProductResponse
from app.services.llm_service import llm_service

router = APIRouter(prefix="/compare", tags=["Compare"])

@router.post("", response_model=CompareResponse, summary="Compare up to 4 products side-by-side")
def compare_products(request: CompareRequest, db: Session = Depends(get_db)):
    if not request.product_ids or len(request.product_ids) < 1:
        raise HTTPException(status_code=400, detail="Provide between 1 and 4 product IDs to compare.")
    if len(request.product_ids) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 products allowed for comparison.")

    prods = db.query(ProductModel).filter(ProductModel.id.in_(request.product_ids)).all()
    if not prods:
        raise HTTPException(status_code=404, detail="No matching products found for comparison.")

    prod_dicts = [p.to_dict() for p in prods]
    
    # Generate structured comparison summary
    price_comp = {p["id"]: {"price": p["price"], "oldPrice": p.get("oldPrice"), "discount": p.get("discountPercentage", 0)} for p in prod_dicts}
    rating_comp = {p["id"]: {"rating": p["rating"], "reviews": p["reviews"]} for p in prod_dicts}
    specs_comp = {p["id"]: p.get("specifications", {}) for p in prod_dicts}
    
    summary = ComparisonSummary(
        price=price_comp,
        rating=rating_comp,
        specifications=specs_comp,
        highlights=[f"{p['name']} is rated {p['rating']}★" for p in prod_dicts]
    )

    return CompareResponse(
        products=[ProductResponse(**p) for p in prod_dicts],
        comparison=summary
    )

@router.post("/explain", response_model=CompareResponse, summary="AI-generated comparison explanation")
@router.post("/insights", response_model=CompareResponse, summary="AI-generated comparison explanation")
async def explain_comparison(request: CompareExplainRequest, db: Session = Depends(get_db)):
    if not request.product_ids:
        raise HTTPException(status_code=400, detail="Provide product IDs to compare.")

    prods = db.query(ProductModel).filter(ProductModel.id.in_(request.product_ids)).all()
    if not prods:
        raise HTTPException(status_code=404, detail="Products not found.")

    prod_dicts = [p.to_dict() for p in prods]
    explanation = await llm_service.explain_comparison(
        prod_dicts, 
        request.query or "Compare these products",
        language=request.language or "english"
    )

    price_comp = {p["id"]: {"price": p["price"], "oldPrice": p.get("oldPrice")} for p in prod_dicts}
    rating_comp = {p["id"]: {"rating": p["rating"], "reviews": p["reviews"]} for p in prod_dicts}

    summary = ComparisonSummary(
        price=price_comp,
        rating=rating_comp,
        specifications={p["id"]: p.get("specifications", {}) for p in prod_dicts},
        highlights=[f"{p['name']} is rated {p['rating']}★" for p in prod_dicts]
    )

    return CompareResponse(
        products=[ProductResponse(**p) for p in prod_dicts],
        comparison=summary,
        explanation=explanation
    )
