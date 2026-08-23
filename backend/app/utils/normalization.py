import re
from typing import Tuple, Optional, Dict, Any

CATEGORY_MAP = {
    "laptop": ("Electronics", "Laptops"),
    "laptops": ("Electronics", "Laptops"),
    "computer": ("Electronics", "Laptops"),
    "notebook": ("Electronics", "Laptops"),
    "phone": ("Electronics", "Smartphones"),
    "phones": ("Electronics", "Smartphones"),
    "mobile": ("Electronics", "Smartphones"),
    "smartphone": ("Electronics", "Smartphones"),
    "smartphones": ("Electronics", "Smartphones"),
    "earbuds": ("Electronics", "Headphones"),
    "earphone": ("Electronics", "Headphones"),
    "earphones": ("Electronics", "Headphones"),
    "headphones": ("Electronics", "Headphones"),
    "headphone": ("Electronics", "Headphones"),
    "headset": ("Electronics", "Headphones"),
    "audio": ("Electronics", "Audio"),
    "speaker": ("Electronics", "Audio"),
    "speakers": ("Electronics", "Audio"),
    "monitor": ("Electronics", "Monitors"),
    "monitors": ("Electronics", "Monitors"),
    "screen": ("Electronics", "Monitors"),
    "display": ("Electronics", "Monitors"),
    "tablet": ("Electronics", "Tablets"),
    "tablets": ("Electronics", "Tablets"),
    "ipad": ("Electronics", "Tablets"),
    "shirt": ("Fashion", "Shirts"),
    "shirts": ("Fashion", "Shirts"),
    "tshirt": ("Fashion", "T-Shirts"),
    "t-shirt": ("Fashion", "T-Shirts"),
    "t-shirts": ("Fashion", "T-Shirts"),
    "tee": ("Fashion", "T-Shirts"),
    "jeans": ("Fashion", "Jeans"),
    "pant": ("Fashion", "Jeans"),
    "pants": ("Fashion", "Jeans"),
    "trousers": ("Fashion", "Formal Wear"),
    "blazer": ("Fashion", "Formal Wear"),
    "suit": ("Fashion", "Formal Wear"),
    "hoodie": ("Fashion", "Hoodies"),
    "hoodies": ("Fashion", "Hoodies"),
    "shoe": ("Footwear", "Running Shoes"),
    "shoes": ("Footwear", "Running Shoes"),
    "running shoes": ("Footwear", "Running Shoes"),
    "sneaker": ("Footwear", "Casual Shoes"),
    "sneakers": ("Footwear", "Casual Shoes"),
    "boots": ("Footwear", "Sports Shoes"),
    "formal shoes": ("Footwear", "Formal Shoes"),
    "backpack": ("Accessories", "Backpacks"),
    "backpacks": ("Accessories", "Backpacks"),
    "bag": ("Accessories", "Backpacks"),
    "bags": ("Accessories", "Backpacks"),
    "watch": ("Accessories", "Watches"),
    "watches": ("Accessories", "Watches"),
    "wallet": ("Accessories", "Wallets"),
    "wallets": ("Accessories", "Wallets"),
    "sunglasses": ("Accessories", "Smart Wearables"),
    "fitness tracker": ("Accessories", "Smart Wearables"),
    "lamp": ("Home & Lifestyle", "Desk Lamps"),
    "lamps": ("Home & Lifestyle", "Desk Lamps"),
    "desk lamp": ("Home & Lifestyle", "Desk Lamps"),
    "light": ("Home & Lifestyle", "Desk Lamps"),
    "blender": ("Home & Lifestyle", "Kitchen"),
    "mixer": ("Home & Lifestyle", "Kitchen"),
    "bottle": ("Home & Lifestyle", "Kitchen"),
    "kettle": ("Home & Lifestyle", "Kitchen"),
    "cushion": ("Home & Lifestyle", "Office Essentials"),
    "diffuser": ("Home & Lifestyle", "Home Decor"),
    "gift": ("Gifts", "Gift Sets"),
    "gifts": ("Gifts", "Gift Sets"),
    "hamper": ("Gifts", "Hampers"),
    "candle": ("Gifts", "Gift Sets"),
    "journal": ("Gifts", "Personalised Gifts"),
}

# Telugu term mappings to English concepts
TELUGU_CONCEPT_MAP = {
    "చదువు": "study",
    "కోడింగ్": "coding",
    "ప్రోగ్రామింగ్": "programming",
    "గేమింగ్": "gaming",
    "ఆఫీస్": "office",
    "మంచి": "good quality",
    "తక్కువ ధర": "budget friendly",
    "బాగుండాలి": "high rating",
    "ఫోన్": "phone",
    "లాప్‌టాప్": "laptop",
    "ల్యాప్‌టాప్": "laptop",
    "ఇయర్ బడ్స్": "earbuds",
    "షూస్": "shoes",
    "బ్యాగ్": "backpack",
    "వాచ్": "watch",
    "చొక్కా": "shirt",
    "బట్టలు": "clothes"
}

def extract_price_range(query: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Extracts min and max price from queries like:
    - 'under 60000', 'below 50k', '60k lopu', '60000 లోపు', '200000 lopu', '2 lakhs lopu', 'around 30k', '30k to 50k'
    """
    text = query.lower()
    
    # 1. Range expressions: "30k to 50k", "30000 - 50000", "20k nundi 40k"
    range_match = re.search(r'(\d+)(k|\s*,\s*\d{3}|\s*000)?\s*(?:to|-|nundi|varku)\s*(\d+)(k|\s*,\s*\d{3}|\s*000)?', text)
    if range_match:
        val1 = int(range_match.group(1))
        unit1 = range_match.group(2)
        if unit1 and 'k' in unit1:
            val1 *= 1000
        elif val1 < 200:  # e.g., "30 to 50k" -> val1 is 30k
            val1 *= 1000
            
        val2 = int(range_match.group(3))
        unit2 = range_match.group(4)
        if unit2 and 'k' in unit2:
            val2 *= 1000
        elif val2 < 200:
            val2 *= 1000
            
        return float(min(val1, val2)), float(max(val1, val2))

    # 2. Lakhs expressions: "2 lakhs", "2 lakh", "2.5 lakhs", "2 లక్షలు", "2 లక్షల", "1.5 lac"
    lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakhs?|lac|lacs?|లక్షలు|లక్షల|లక్ష)', text)
    if lakh_match:
        return None, float(float(lakh_match.group(1)) * 100000)

    # 3. Thousands / vela expressions: "60 vela", "60 వేల", "60 వేలు"
    vela_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:vela|velu|వేల|వేలు)', text)
    if vela_match:
        return None, float(float(vela_match.group(1)) * 1000)

    # 4. 'k' abbreviations: "60k", "200k", "5k", "60k lopu"
    k_match = re.search(r'(\d+)\s*k\b', text)
    if k_match:
        return None, float(int(k_match.group(1)) * 1000)

    # 5. Price with keyword or symbol context: "under 60000", "200000 lopu", "₹54,990", "<= 50000"
    num_match = re.search(r'(?:under|below|less than|lopu|lo|budget|max|within|₹|rs\.?|inr|<=)?\s*(?:₹|rs\.?|inr)?\s*(\d+[\d,]*)\s*(?:under|below|lopu|lo|dharalo|budget|లోపు|వరకు)?', text)
    if num_match:
        num_str = num_match.group(1).replace(',', '')
        if num_str.isdigit():
            val = float(num_str)
            # Only multiply by 1000 if number is small (e.g. "60 lopu" where 60 means 60k)
            if val < 500 and any(w in text for w in ['lopu', 'under', 'below', 'budget', 'వరకు', 'లోపు']):
                val *= 1000
            return None, val

    return None, None

UNSUPPORTED_CATEGORIES = [
    "camera", "dslr", "cameras", "washing machine", "refrigerator", "fridge",
    "ac", "air conditioner", "car", "bike", "cycle", "tv", "television",
    "drone", "microwave", "oven", "guitar", "piano", "printer"
]

def normalize_query_text(query: str) -> Dict[str, Any]:
    """
    Extracts category, price limits, use cases and normalized English keywords
    from English, Telugu and Roman Telugu text.
    """
    normalized = query.lower()
    
    # Translate known Telugu script words
    for tel, eng in TELUGU_CONCEPT_MAP.items():
        normalized = normalized.replace(tel, f" {eng} ")
        
    min_price, max_price = extract_price_range(query)
    
    # Check for unsupported categories first
    for unc in UNSUPPORTED_CATEGORIES:
        if re.search(rf'\b{re.escape(unc)}\b', normalized):
            return {
                "normalized_text": normalized,
                "category": "UNSUPPORTED",
                "subcategory": unc,
                "min_price": min_price,
                "max_price": max_price,
                "use_cases": []
            }

    category = None
    subcategory = None
    
    # Check for categories in the normalized query
    for kw, (cat, subcat) in CATEGORY_MAP.items():
        if re.search(rf'\b{re.escape(kw)}\b', normalized):
            category = cat
            subcategory = subcat
            break
            
    # Extract brands
    brands = []
    brand_keywords = ["apple", "macbook", "asus", "acer", "hp", "dell", "lenovo", "samsung", "oneplus", "realme", "redmi", "xiaomi", "sony", "aerobuds", "sonicbeam", "pixelview", "zenbook"]
    for b in brand_keywords:
        if re.search(rf'\b{re.escape(b)}\b', normalized):
            if b == "macbook":
                brands.append("Apple")
                if not category:
                    category = "Electronics"
                    subcategory = "Laptops"
            else:
                brands.append(b.capitalize())

    # Extract RAM
    ram = None
    ram_match = re.search(r'(\d+)\s*(?:gb)?\s*ram', normalized)
    if ram_match:
        ram = f"{ram_match.group(1)}GB RAM"
    elif "16gb" in normalized or "16 gb" in normalized:
        ram = "16GB RAM"
    elif "8gb" in normalized or "8 gb" in normalized:
        ram = "8GB RAM"
    elif "32gb" in normalized or "32 gb" in normalized:
        ram = "32GB RAM"

    # Extract Storage
    storage = None
    if "1tb" in normalized or "1 tb" in normalized:
        storage = "1TB SSD"
    elif "512gb" in normalized or "512 gb" in normalized:
        storage = "512GB SSD"
    elif "256gb" in normalized or "256 gb" in normalized:
        storage = "256GB SSD"

    # Extract Display
    display = None
    if "oled" in normalized:
        display = "OLED"
    elif "4k" in normalized or "uhd" in normalized:
        display = "4K"
    elif "amoled" in normalized:
        display = "AMOLED"
    elif "120hz" in normalized or "144hz" in normalized:
        display = "High Refresh Rate"

    # Strict constraint detection
    strict_words = ["compulsory", "must", "strictly", "తప్పనిసరిగా", "only", "exact", "కచ్చితంగా", "ఖచ్చితంగా"]
    is_strict = any(w in normalized for w in strict_words)
    strict_constraints = []
    if is_strict:
        if ram: strict_constraints.append(ram)
        if storage: strict_constraints.append(storage)
        if display: strict_constraints.append(display)
        if max_price: strict_constraints.append(f"Max ₹{max_price:,.0f}")

    # Extract use cases
    use_cases = []
    if any(w in normalized for w in ["coding", "programming", "developer", "software", "python", "java"]):
        use_cases.append("coding")
    if any(w in normalized for w in ["gaming", "gamer", "graphics", "game"]):
        use_cases.append("gaming")
    if any(w in normalized for w in ["student", "college", "school", "study", "education"]):
        use_cases.append("student")
    if any(w in normalized for w in ["office", "work", "wfh", "business", "workstation"]):
        use_cases.append("office")
    if any(w in normalized for w in ["running", "sports", "gym", "workout"]):
        use_cases.append("running")
    if any(w in normalized for w in ["gift", "present", "birthday", "anniversary"]):
        use_cases.append("gift")

    return {
        "original_query": query,
        "normalized_text": normalized.strip(),
        "category": category,
        "subcategory": subcategory,
        "min_price": min_price,
        "max_price": max_price,
        "brands": brands,
        "ram": ram,
        "storage": storage,
        "display": display,
        "strict_constraints": strict_constraints,
        "is_strict": is_strict,
        "use_cases": use_cases
    }
