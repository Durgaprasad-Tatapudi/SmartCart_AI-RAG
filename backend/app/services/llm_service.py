import os
import json
import re
import httpx
from typing import List, Dict, Any, Optional, Tuple
from app.core.config import settings
from app.core.logging import logger
from app.schemas.search import ShoppingIntent
from app.schemas.assistant import FollowUpQuestion, ChatMessage
from app.utils.language import detect_language
from app.utils.normalization import normalize_query_text

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.base_url = settings.OPENROUTER_BASE_URL
        
        # Load system prompts
        prompt_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        try:
            with open(os.path.join(prompt_dir, "assistant_system.txt"), "r", encoding="utf-8") as f:
                self.assistant_system_prompt = f.read()
            with open(os.path.join(prompt_dir, "intent_extraction.txt"), "r", encoding="utf-8") as f:
                self.intent_system_prompt = f.read()
            with open(os.path.join(prompt_dir, "compare_explain.txt"), "r", encoding="utf-8") as f:
                self.compare_system_prompt = f.read()
        except Exception as e:
            logger.warning(f"Failed to load prompt files ({e}), using defaults.")
            self.assistant_system_prompt = "You are SmartCart AI. Only use provided product data. Respond in user language."
            self.intent_system_prompt = "Extract shopping intent JSON."
            self.compare_system_prompt = "Compare the provided products factually."

    async def _call_openrouter(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> Optional[str]:
        """Calls OpenRouter chat completions API with multi-model failover."""
        if not self.api_key:
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "SmartCart AI"
        }

        models_to_try = list(dict.fromkeys([
            "openrouter/auto",
            self.model,
            "liquid/lfm-2.5-2.6b:free"
        ]))

        for model in models_to_try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 500
            }

            try:
                async with httpx.AsyncClient(timeout=12.0) as client:
                    resp = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        logger.warning(f"OpenRouter model {model} returned status {resp.status_code}. Trying next model...")
            except Exception as e:
                logger.warning(f"OpenRouter call failed for {model} ({e}). Trying next model...")

        return None

    async def extract_intent(self, query: str, history: List[ChatMessage] = []) -> ShoppingIntent:
        """Extracts structured ShoppingIntent using OpenRouter LLM or deterministic fallback."""
        detected_lang = detect_language(query)
        deterministic_info = normalize_query_text(query)
        
        # Prepare fallback default
        fallback_intent = ShoppingIntent(
            query=query,
            normalized_query=deterministic_info["normalized_text"],
            language=detected_lang,
            category=deterministic_info["category"],
            subcategory=deterministic_info["subcategory"],
            min_price=deterministic_info["min_price"],
            max_price=deterministic_info["max_price"],
            brands=deterministic_info.get("brands", []),
            ram=deterministic_info.get("ram"),
            storage=deterministic_info.get("storage"),
            display=deterministic_info.get("display"),
            strict_constraints=deterministic_info.get("strict_constraints", []),
            is_strict=deterministic_info.get("is_strict", False),
            use_case=deterministic_info["use_cases"],
            cheaper_request="cheaper" in query.lower() or "takkava" in query.lower()
        )

        # If category or price is already detected by NLP normalizer, use it immediately
        if deterministic_info["category"] or deterministic_info["max_price"] or not self.api_key:
            return fallback_intent

        messages = [
            {"role": "system", "content": self.intent_system_prompt},
            {"role": "user", "content": f"Extract intent for query: '{query}'\nDetected language: {detected_lang}"}
        ]

        llm_output = await self._call_openrouter(messages, temperature=0.1)
        if not llm_output:
            return fallback_intent

        try:
            # Clean possible markdown wrapping
            cleaned = re.sub(r'^```(?:json)?\s*', '', llm_output.strip())
            cleaned = re.sub(r'\s*```$', '', cleaned)
            data = json.loads(cleaned)
            return ShoppingIntent(**data)
        except Exception as e:
            logger.warning(f"Failed to parse LLM intent JSON ({e}): {llm_output}")
            return fallback_intent

    async def generate_assistant_response(
        self,
        query: str,
        intent: ShoppingIntent,
        products: List[Dict[str, Any]],
        history: List[ChatMessage] = [],
        language: str = "english",
        result_type: str = "EXACT_MATCH"
    ) -> Tuple[str, Optional[FollowUpQuestion], List[str]]:
        """Generates conversational response grounded strictly in retrieved products.
        Adapts tone based on result_type: EXACT_MATCH, NO_EXACT_BUT_NEARBY, NO_RELEVANT_PRODUCTS.
        """
        
        lang = language.lower() if language else (intent.language or "english")
        is_telugu = lang in ["telugu", "te"]

        # 1. Fallback / deterministic response generator
        def get_fallback_response():
            if not products:
                unsupported_name = intent.subcategory or "that item"
                if intent.category == "UNSUPPORTED":
                    if is_telugu:
                        msg = f"మీకు '{unsupported_name}' కావాలని అర్థమైంది. ప్రస్తుతం SmartCart catalogue లో {unsupported_name} అందుబాటులో లేవు. అందువల్ల సంబంధం లేని products ని recommend చేయడం లేదు. ప్రస్తుతం Laptops, Smartphones, Earbuds, Monitors, Fashion మరియు Home essentials అందుబాటులో ఉన్నాయి."
                    else:
                        msg = f"I understand you're looking for '{unsupported_name}'. Currently, SmartCart's catalogue doesn't include {unsupported_name}, so I won't recommend unrelated products. We currently offer Laptops, Smartphones, Audio/Earbuds, Monitors, Fashion, and Home essentials."
                else:
                    if is_telugu:
                        cat_name = intent.subcategory or intent.category or "ఉత్పత్తులు"
                        if intent.max_price:
                            msg = f"మీకు ₹{intent.max_price:,.0f} లోపు {cat_name} కావాలని అర్థమైంది. ప్రస్తుతం మా catalogue లో ఈ budget లో సరైన options అందుబాటులో లేవు."
                        else:
                            msg = f"మీ శోధనకు సరిపోయే ఉత్పత్తులు ప్రస్తుతం అందుబాటులో లేవు. దయచేసి వేరే category లేదా budget ప్రయత్నించండి."
                    else:
                        cat_name = intent.subcategory or intent.category or "products"
                        if intent.max_price:
                            msg = f"I understand you're looking for {cat_name} under ₹{intent.max_price:,.0f}. Unfortunately, we don't have suitable options in this budget range right now."
                        else:
                            msg = f"I couldn't find suitable matches for '{query}' in our current catalogue. Try adjusting your budget or browsing different categories."
                
                follow_up = None
                suggestions = ["Best laptops under 60k", "Top rated earbuds", "Gaming laptops"]
                return msg, follow_up, suggestions

            # Products found — generate result-type-aware message
            n = len(products)
            cat_name = intent.subcategory or intent.category or "products"

            if result_type == "NO_EXACT_BUT_NEARBY":
                if is_telugu:
                    msg = f"మీకు ₹{intent.max_price:,.0f} లోపు {cat_name} కావాలని అర్థమైంది. ప్రస్తుతం ఆ budget లో exact match లేదు. కానీ మీ budget కి దగ్గరగా ఉన్న కొన్ని మంచి options ఇవి."
                else:
                    msg = f"I understand you need {cat_name} under ₹{intent.max_price:,.0f}. We don't have exact matches within that budget right now, but here are {n} strong alternatives closest to your price range."
            else:
                # EXACT_MATCH
                if is_telugu:
                    if intent.max_price:
                        msg = f"మీకు ₹{intent.max_price:,.0f} లోపు {cat_name} కావాలని అర్థమైంది. Processor, RAM మరియు performance ని priority గా తీసుకుని ఈ {n} options ని select చేశాను."
                    else:
                        msg = f"మీ అవసరాలకు తగిన {n} ఉత్తమ {cat_name} options ని ఎంపిక చేశాను. వీటి వివరాలు క్రింద చూడవచ్చు."
                else:
                    if intent.max_price:
                        msg = f"I found {n} top-rated {cat_name} options within your ₹{intent.max_price:,.0f} budget, prioritized by specifications, ratings, and value."
                    else:
                        msg = f"Based on your requirements, I've selected {n} strong {cat_name} options from our catalogue."

            follow_up = None
            if not intent.category and not intent.use_case:
                follow_up = FollowUpQuestion(
                    question="What will you primarily use it for?" if not is_telugu else "మీరు దీన్ని ప్రధానంగా ఎందుకు ఉపయోగిస్తారు?",
                    options=["Coding & Work", "Gaming", "Daily Entertainment", "College Study"],
                    context_field="use_case"
                )

            suggestions = [
                "Compare top products",
                "Show cheaper alternatives",
                "View detailed specifications"
            ]
            return msg, follow_up, suggestions

        if not products or intent.category == "UNSUPPORTED":
            return get_fallback_response()

        if not self.api_key:
            return get_fallback_response()

        # Build grounded catalog context for LLM
        product_summaries = []
        for idx, p in enumerate(products[:5], 1):
            specs_str = ", ".join(p.get("specs", []))
            budget_tag = ""
            if p.get("budget_status") == "above_budget" and p.get("budget_difference"):
                budget_tag = f" [₹{p['budget_difference']:,.0f} ABOVE BUDGET]"
            product_summaries.append(
                f"{idx}. {p.get('name')} (Brand: {p.get('brand')}, Price: ₹{p.get('price')}{budget_tag}, Rating: {p.get('rating')}/5, Specs: {specs_str})"
            )
        catalog_context = "\n".join(product_summaries)

        target_lang_str = "Telugu (తెలుగు)" if is_telugu else "English"

        result_context = ""
        if result_type == "NO_EXACT_BUT_NEARBY":
            result_context = f"""
IMPORTANT CONTEXT: The user's budget was ₹{intent.max_price:,.0f} but NO products exist within that budget.
The products listed below are the CLOSEST alternatives ABOVE the budget.
You MUST:
1. Acknowledge the user's budget clearly
2. Explain that exact matches are not available
3. Present these as "closest alternatives near your budget"
4. NEVER claim these products are within their budget
"""

        prompt = f"""User query: "{query}"
Target Response Language: {target_lang_str}
Detected Intent: Category={intent.category}, Max Price={intent.max_price}, Use cases={intent.use_case}
Result Status: {result_type}
{result_context}
RELEVANT CATALOGUE PRODUCTS:
{catalog_context}

Please generate:
1. A concise, helpful shopping recommendation (2 to 4 sentences) explaining why these options match their requirement.
2. If Target Language is Telugu, generate the explanation strictly in Telugu script (తెలుగు), keeping technical specs (like 16GB RAM, 512GB SSD) in English.
3. ONLY reference facts from the catalogue context above.
"""

        messages = [
            {"role": "system", "content": self.assistant_system_prompt},
            {"role": "user", "content": prompt}
        ]

        llm_reply = await self._call_openrouter(messages, temperature=0.3)
        if not llm_reply:
            return get_fallback_response()

        _, follow_up, suggestions = get_fallback_response()
        return llm_reply.strip(), follow_up, suggestions

    async def explain_comparison(self, products: List[Dict[str, Any]], query: str = "Compare these products", language: str = "english") -> str:
        """Generates grounded factual comparison explanation in requested language."""
        if not products:
            return "No products selected for comparison."

        is_telugu = language.lower() in ["te", "telugu"]
        lang_instruction = "Respond entirely in Telugu (తెలుగు). Do not invent specifications." if is_telugu else "Respond in English. Do not invent specifications."

        if not self.api_key:
            names = [p.get("name") for p in products]
            prices = [f"{p.get('name')}: ₹{p.get('price'):,}" for p in products]
            if is_telugu:
                return f"{', '.join(names)} పోలిక:\n- ధరల వివరాలు: {', '.join(prices)}.\nప్రతి ఉత్పత్తి విభిన్న అవసరాలు మరియు బడ్జెట్లకు తగిన ఫీచర్లను అందిస్తుంది."
            return f"Comparison between {', '.join(names)}:\n- Pricing: {', '.join(prices)}.\nEach product provides distinct features and value for different budgets and use cases."

        product_details = []
        for p in products:
            product_details.append(
                f"- Name: {p.get('name')} | Brand: {p.get('brand')} | Price: ₹{p.get('price')} (Old: ₹{p.get('oldPrice', p.get('price'))}) | Rating: {p.get('rating')}/5 ({p.get('reviews')} reviews)\n  Specs: {', '.join(p.get('specs', []))}\n  Description: {p.get('description')}"
            )

        messages = [
            {"role": "system", "content": self.compare_system_prompt + f"\nLanguage Instruction: {lang_instruction}"},
            {"role": "user", "content": f"User query: {query}\nTarget Language: {language}\n\nProducts to compare:\n" + "\n".join(product_details)}
        ]

        output = await self._call_openrouter(messages, temperature=0.2)
        return output or "Products compared based on specifications and pricing."

llm_service = LLMService()
