from typing import List, Dict, Any, Tuple
from app.schemas.search import ShoppingIntent, RankedProduct
from app.schemas.product import ProductResponse

class RankingService:
    def rank_products(
        self,
        products: List[Dict[str, Any]],
        intent: ShoppingIntent,
        vector_scores: Dict[str, float] = {},
        allow_over_budget: bool = False
    ) -> List[RankedProduct]:
        """
        Ranks product candidates using deterministic multi-factor scoring formula:
        Score = 0.30 * semantic + 0.20 * category_match + 0.20 * budget_fit + 0.15 * spec_match + 0.15 * use_case_match
        
        When allow_over_budget=True, over-budget products are kept with a penalty instead of being filtered out.
        Each product gets a grounded, personalized `why_recommended` reason.
        """
        ranked_list = []
        
        for p in products:
            pid = p.get("id")
            score = 0.0
            reasons = []

            # 1. Semantic Similarity Score (0.0 to 1.0)
            semantic_score = vector_scores.get(pid, 0.7)
            score += 0.30 * semantic_score

            # Strict subcategory constraint if specified
            if intent.subcategory:
                sub_lower = intent.subcategory.lower()
                p_sub = p.get("subcategory", "").lower()
                if sub_lower not in p_sub and p_sub not in sub_lower:
                    continue
            elif intent.category:
                cat_lower = intent.category.lower()
                p_cat = p.get("category", "").lower()
                p_sub = p.get("subcategory", "").lower()
                if cat_lower not in p_cat and cat_lower not in p_sub and p_cat not in cat_lower and p_sub not in cat_lower:
                    continue

            # Budget handling
            price = float(p.get("price", 0))
            budget_status = "within_budget"
            budget_difference = 0.0

            if intent.max_price:
                if price > intent.max_price:
                    if not allow_over_budget:
                        continue
                    budget_status = "above_budget"
                    budget_difference = price - intent.max_price
                    over_ratio = budget_difference / intent.max_price
                    if over_ratio > 1.2:
                        continue
                    budget_fit = max(0.0, 0.5 - (over_ratio * 0.3))
                    reasons.append(f"₹{budget_difference:,.0f} above your ₹{intent.max_price:,.0f} budget")
                else:
                    budget_fit = 1.0
                    reasons.append(f"Within budget (₹{price:,.0f} ≤ ₹{intent.max_price:,.0f})")
            else:
                budget_fit = 0.8

            if intent.min_price and price < intent.min_price:
                continue

            # 2. Category Match Score
            cat_match = 1.0 if (intent.category and intent.category.lower() in p.get("category", "").lower()) else 0.8
            score += 0.20 * cat_match

            # 3. Budget Fit
            score += 0.20 * budget_fit

            p_tags = [t.lower() for t in p.get("tags", [])]
            p_specs = [s.lower() for s in p.get("specs", [])]
            p_desc = (p.get("description") or "").lower()
            combined_text = " ".join(p_tags + p_specs + [p_desc, p.get("name", "").lower(), p.get("brand", "").lower()])

            # 4. Specification Match (RAM, Storage, Display, Brand)
            spec_score = 0.5
            spec_matches = []
            
            # Brand match
            if intent.brands:
                for b in intent.brands:
                    if b.lower() in (p.get("brand") or "").lower() or b.lower() in p.get("name", "").lower():
                        spec_score += 0.3
                        spec_matches.append(b)
                        reasons.append(f"Brand: {b}")

            # RAM match (e.g. 16GB)
            if intent.ram:
                ram_str = intent.ram.lower().replace(" ", "")
                if "16gb" in ram_str and any("16gb" in s.replace(" ", "") for s in p_specs + p_tags):
                    spec_score += 0.3
                    spec_matches.append("16GB RAM")
                    reasons.append("16GB RAM for multitasking")
                elif "8gb" in ram_str and any("8gb" in s.replace(" ", "") for s in p_specs + p_tags):
                    spec_score += 0.2
                    spec_matches.append("8GB RAM")

            # Storage match (e.g. 512GB, 1TB)
            if intent.storage:
                storage_str = intent.storage.lower().replace(" ", "")
                if "1tb" in storage_str and any("1tb" in s.replace(" ", "") for s in p_specs + p_tags):
                    spec_score += 0.3
                    spec_matches.append("1TB SSD")
                    reasons.append("1TB high-capacity SSD")
                elif "512gb" in storage_str and any("512gb" in s.replace(" ", "") for s in p_specs + p_tags):
                    spec_score += 0.2
                    spec_matches.append("512GB SSD")
                    reasons.append("512GB fast SSD")

            # Display match (e.g. OLED, 4K)
            if intent.display:
                disp_lower = intent.display.lower()
                if disp_lower in combined_text:
                    spec_score += 0.3
                    spec_matches.append(intent.display)
                    reasons.append(f"{intent.display} display")

            score += 0.15 * min(spec_score, 1.0)

            # 5. Use-case & Feature Match (0.0 to 1.0)
            use_case_score = 0.5
            uc_matches = []
            for uc in intent.use_case:
                if uc.lower() in combined_text:
                    uc_matches.append(uc.capitalize())
            if uc_matches:
                use_case_score = 1.0
                reasons.append(f"Optimized for {', '.join(uc_matches)}")
            score += 0.15 * use_case_score

            # Rating & Popularity Bonus
            rating = float(p.get("rating", 4.0))
            reviews = int(p.get("reviews", 0))
            if rating >= 4.5:
                score += 0.05
                reasons.append(f"{rating}★ rating ({reviews:,} reviews)")

            # Generate why_recommended from top attributes
            why_recommended = self._generate_why(p, intent, uc_matches, spec_matches, budget_status)

            p["why_recommended"] = why_recommended
            p["budget_status"] = budget_status
            p["budget_difference"] = budget_difference if budget_status == "above_budget" else None

            ranked_list.append(
                RankedProduct(
                    product=ProductResponse(**p),
                    match_score=round(score, 3),
                    match_reasons=reasons[:3]
                )
            )

        # Sort descending by match score
        ranked_list.sort(key=lambda x: x.match_score, reverse=True)
        return ranked_list

    def _generate_why(self, product: Dict, intent: ShoppingIntent, use_case_matches: list, spec_matches: list, budget_status: str) -> str:
        """Generates a specific, grounded why_recommended string based on product attributes and user intent."""
        specs = product.get("specs", [])
        name = product.get("name", "")
        price = product.get("price", 0)
        rating = product.get("rating", 0)
        category = product.get("subcategory") or product.get("category", "")
        
        highlights = []
        for spec in specs[:3]:
            spec_lower = spec.lower()
            if any(kw in spec_lower for kw in ["ram", "ssd", "core", "ryzen", "m1", "m2", "m3", "snapdragon"]):
                highlights.append(spec)
            elif any(kw in spec_lower for kw in ["anc", "noise cancel", "battery", "ipx", "bluetooth"]):
                highlights.append(spec)
            elif any(kw in spec_lower for kw in ["4k", "uhd", "144hz", "amoled", "oled"]):
                highlights.append(spec)
        
        if not highlights:
            highlights = specs[:2] if specs else []
        
        parts = []
        if highlights:
            parts.append(" + ".join(highlights[:3]))
        
        if use_case_matches:
            uses = ", ".join(use_case_matches)
            parts.append(f"suitable for {uses}")
        elif spec_matches:
            parts.append(f"matches {', '.join(spec_matches)}")
            
        if rating >= 4.5:
            parts.append(f"{rating}★ rated")
        
        if budget_status == "above_budget":
            diff = price - (intent.max_price or 0)
            parts.append(f"₹{diff:,.0f} above budget")
        elif intent.max_price and price <= intent.max_price:
            parts.append("within budget")
        
        if parts:
            return ". ".join(parts[:3]) + "."
        return f"Strong option in {category}."

ranking_service = RankingService()
