from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import ProductModel, SearchHistoryModel
from app.schemas.search import SearchRequest, SearchResponse, ShoppingIntent
from app.schemas.product import ProductResponse
from app.services.llm_service import llm_service
from app.services.vector_service import vector_service
from app.services.ranking_service import ranking_service
from app.core.logging import logger

class SearchService:
    async def search(self, db: Session, request: SearchRequest) -> SearchResponse:
        """
        Executes end-to-end multilingual search pipeline with 3-level fallback:
        Level 1: Exact match (category + budget + constraints)
        Level 2: Category + budget relaxed (keeps category, widens budget)
        Level 3: Nearest alternatives above budget (clearly labeled)
        """
        query = request.query
        
        # 1. Log search history if session provided
        if request.session_id:
            try:
                hist = SearchHistoryModel(session_id=request.session_id, query=query)
                db.add(hist)
                db.commit()
            except Exception as e:
                logger.warning(f"Could not save search history: {e}")

        # 2. Extract structured shopping intent
        intent = await llm_service.extract_intent(query)
        
        # Override intent with explicit query params if provided
        if request.category:
            intent.category = request.category
        if request.min_price is not None:
            intent.min_price = request.min_price
        if request.max_price is not None:
            intent.max_price = request.max_price

        # If query is for an unsupported category, return empty results
        if intent.category == "UNSUPPORTED":
            return SearchResponse(
                query=query,
                language=intent.language,
                intent=intent,
                results=[],
                products=[],
                total=0,
                result_type="NO_RELEVANT_PRODUCTS",
                explanation=f"I couldn't find {intent.subcategory or 'this category'} in the current SmartCart catalogue."
            )

        # 3. LEVEL 1: Vector search with all constraints (category + budget)
        vector_hits = vector_service.search(
            query=intent.normalized_query or query,
            limit=request.limit * 2,
            category=intent.category,
            min_price=intent.min_price,
            max_price=intent.max_price
        )

        vector_scores = {}
        matched_product_ids = []

        if vector_hits:
            for hit in vector_hits:
                pid = hit["product_id"]
                matched_product_ids.append(pid)
                vector_scores[pid] = hit["score"]

        # Hydrate from SQLite
        candidate_products = []
        if matched_product_ids:
            db_products = db.query(ProductModel).filter(ProductModel.id.in_(matched_product_ids)).all()
            candidate_products = [p.to_dict() for p in db_products]
            
        if not candidate_products:
            # Fallback SQL search (Level 1 SQL)
            q_builder = db.query(ProductModel)
            if intent.category:
                q_builder = q_builder.filter(ProductModel.category.ilike(f"%{intent.category}%"))
            if intent.max_price:
                q_builder = q_builder.filter(ProductModel.price <= intent.max_price)
            if intent.min_price:
                q_builder = q_builder.filter(ProductModel.price >= intent.min_price)
            
            db_fallbacks = q_builder.limit(request.limit).all()
            candidate_products = [p.to_dict() for p in db_fallbacks]

        # Rank Level 1 results (strict budget filtering)
        ranked = ranking_service.rank_products(
            products=candidate_products,
            intent=intent,
            vector_scores=vector_scores,
            allow_over_budget=False
        )

        result_type = "EXACT_MATCH"
        budget_note = None

        # 4. LEVEL 2 & 3: If no results found within budget AND a budget was specified
        if not ranked and intent.max_price and intent.category != "UNSUPPORTED":
            logger.info(f"Level 1 returned 0 results for budget ₹{intent.max_price:,.0f}. Trying Level 2/3 near-budget fallback.")
            
            # Re-search without price filter (vector)
            wider_hits = vector_service.search(
                query=intent.normalized_query or query,
                limit=request.limit * 3,
                category=intent.category,
                min_price=None,
                max_price=None
            )

            wider_ids = []
            wider_scores = {}
            if wider_hits:
                for hit in wider_hits:
                    pid = hit["product_id"]
                    wider_ids.append(pid)
                    wider_scores[pid] = hit["score"]

            wider_products = []
            if wider_ids:
                db_wider = db.query(ProductModel).filter(ProductModel.id.in_(wider_ids)).all()
                wider_products = [p.to_dict() for p in db_wider]

            if not wider_products:
                # SQL fallback without price filter
                q_builder = db.query(ProductModel)
                if intent.category:
                    q_builder = q_builder.filter(ProductModel.category.ilike(f"%{intent.category}%"))
                wider_products = q_builder.order_by(ProductModel.price.asc()).limit(request.limit * 2).all()
                wider_products = [p.to_dict() for p in wider_products]

            # Rank with over-budget allowed (ranking_service will penalize + label)
            ranked = ranking_service.rank_products(
                products=wider_products,
                intent=intent,
                vector_scores=wider_scores,
                allow_over_budget=True
            )

            if ranked:
                result_type = "NO_EXACT_BUT_NEARBY"
                closest_price = ranked[0].product.price
                budget_note = f"₹{intent.max_price:,.0f}"
            else:
                result_type = "NO_RELEVANT_PRODUCTS"

        top_ranked = ranked[:request.limit]
        products = [r.product for r in top_ranked]

        # Filters applied summary
        filters_applied = {}
        if intent.category:
            filters_applied["category"] = intent.category
        if intent.max_price:
            filters_applied["max_price"] = intent.max_price
        if intent.min_price:
            filters_applied["min_price"] = intent.min_price

        return SearchResponse(
            query=query,
            language=intent.language,
            intent=intent,
            results=top_ranked,
            products=products,
            total=len(products),
            filters_applied=filters_applied,
            fallback_search=(result_type != "EXACT_MATCH"),
            result_type=result_type,
            budget_note=budget_note
        )

search_service = SearchService()
