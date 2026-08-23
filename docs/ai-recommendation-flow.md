# 🧠 SmartCart AI Recommendation & RAG Pipeline

This document explains the step-by-step intelligence pipeline behind **SmartCart AI-RAG**, detailing how natural language queries are parsed, searched, ranked, and transformed into grounded multilingual sales recommendations.

---

## 1. Step-by-Step AI-RAG Pipeline

```
1. Customer Query: "naku 50000 lopu 16GB RAM laptop kavali"
      │
      ▼
2. Multilingual Normalization & NLP Parsing
   - Detects language: Telugu (Roman script transliteration)
   - Translates Telugu keywords ("lopu" -> "under/max", "kavali" -> "want")
   - Extracts Price Boundary: Max ₹50,000
   - Extracts Hardware Specifications: 16GB RAM
   - Detects Target Subcategory: Laptops
      │
      ▼
3. FastEmbed Dense Vectorization
   - Model: BAAI/bge-small-en-v1.5
   - Query String: "laptops 16GB RAM under 50000"
   - Output: 384-dimensional dense semantic embedding vector
      │
      ▼
4. Qdrant Vector Search & Filtering
   - Collection: smartcart_products
   - Pre-filter: category == "Electronics", subcategory == "Laptops"
   - Cosine Distance Search returns candidate product IDs + similarity scores
      │
      ▼
5. 3-Level Budget & Strict Constraint Search
   - Level 1 (Strict Budget): Filter candidates with Price <= ₹50,000
   - Level 2 (Near-Budget Fallback): If 0 matches, expand to Price <= ₹50,000 * 1.25 with penalty
   - Level 3 (Out-of-Catalog): If category is unsupported (e.g. DSLR camera, washing machine), trigger alert flow
      │
      ▼
6. Multi-Factor Deterministic Ranking
   - Score = 0.30*Semantic + 0.20*Category + 0.20*Budget + 0.15*Specs + 0.15*Use-Case + Rating Bonus
   - Assigns candidates to GROUP A (Direct Matches) or GROUP B (Near-Budget Alternatives)
   - Generates grounded, personalized `why_recommended` justifications
      │
      ▼
7. OpenRouter Multi-Model Grounded LLM Response
   - Prompt includes system grounding constraints: NO hallucinations, use catalog specs strictly
   - Delivers response in natural Telugu script (తెలుగు లిపి) with standard technical English specs
   - Includes structured subscription alert offer if exact match is unavailable
      │
      ▼
8. Client Rendering
   - Salesperson explanation text
   - Group A cards ("మీకు సరిపోయే ఎంపికలు")
   - Group B cards ("మీకు దగ్గరగా ఉన్న ఎంపికలు / ప్రత్యామ్నాయాలు")
   - Inline alert notification box ("🔔 Exact match వచ్చినప్పుడు తెలియజేయండి")
```

---

## 2. Query Normalization & Concept Mapping

SmartCart includes a deterministic NLP translation layer in [`backend/app/utils/normalization.py`](file:///c:/Users/durga/OneDrive/Desktop/smart-cart-ai/backend/app/utils/normalization.py) mapping Telugu terminology to e-commerce concepts:

| Telugu Phrase / Romanization | English Mapping | Action / Extracted Attribute |
| :--- | :--- | :--- |
| `lopu`, `lo`, `లోపు`, `లో` | `under`, `below`, `max` | Extracts upper price boundary (`max_price`) |
| `ekkuva`, `dhaati`, `ఎక్కువ` | `above`, `more than` | Extracts lower price boundary (`min_price`) |
| `takkava`, `thakkuva`, `తక్కువ` | `cheaper`, `budget` | Sets `cheaper_request = True` |
| `kavali`, `chupinchu`, `కావాలి` | `want`, `show me` | Identifies intent type |
| `manchi`, `best`, `మంచి` | `best`, `top rated` | Prioritizes products with rating $\ge 4.5\star$ |
| `coding`, `gaming`, `office`, `student` | Use-case keywords | Matches semantic use-case tags |
| `16gb ram`, `8gb ram`, `32gb ram` | Hardware RAM spec | Enforces RAM matching |
| `512gb ssd`, `1tb ssd`, `256gb ssd` | Storage spec | Enforces NVMe SSD matching |
| `oled`, `4k`, `120hz`, `amoled` | Display spec | Enforces display panel matching |

---

## 3. The 3-Level Budget Fallback Mechanism

Traditional e-commerce search engines return empty pages when an exact budget match is not found. SmartCart prevents dead ends through 3 graceful fallback tiers:

### Level 1: Strict Exact Match
- Returns all items meeting every hardware requirement and falling strictly on or below the user's budget.
- Returns `result_type: EXACT_MATCH`.

### Level 2: Near-Budget Relaxed Match
- If 0 items exist within the strict budget, SmartCart widens the price ceiling by up to 25%–50%.
- Returns candidates tagged with `budget_status: above_budget` and a `+₹X above budget` badge.
- Automatically generates an inline availability alert offer:
  > *"If you strictly want laptops under ₹15,000, set an alert and we will notify you as soon as matching products arrive."*
- Returns `result_type: NO_EXACT_BUT_NEARBY`.

### Level 3: Out-of-Catalog Graceful Handling
- If a customer asks for a category not currently stocked (e.g., DSLR cameras, refrigerators, guitars), the assistant transparently explains:
  > *"ప్రస్తుతం SmartCart catalogue లో camera అందుబాటులో లేవు. కొత్త స్టాక్ వచ్చినప్పుడు మీకు తెలియజేయడానికి alert set చేసుకోండి."*
- Returns `result_type: NO_RELEVANT_PRODUCTS` and displays 0 fake or misleading products.

---

## 4. Multi-Factor Scoring Formula

Candidate products are ranked deterministically:

$$\text{Match Score} = 0.30 \cdot S_{\text{semantic}} + 0.20 \cdot M_{\text{category}} + 0.20 \cdot F_{\text{budget}} + 0.15 \cdot M_{\text{specs}} + 0.15 \cdot M_{\text{use\_case}} + B_{\text{rating}}$$

Where:
- $S_{\text{semantic}} \in [0.0, 1.0]$: Vector cosine similarity score.
- $M_{\text{category}} \in \{0.8, 1.0\}$: Subcategory / Category alignment score.
- $F_{\text{budget}}$:
  $$F_{\text{budget}} = \begin{cases} 1.0 & \text{if } \text{Price} \le \text{Budget} \\ \max\left(0, 0.5 - 0.3 \times \frac{\text{Price} - \text{Budget}}{\text{Budget}}\right) & \text{if Over Budget} \end{cases}$$
- $M_{\text{specs}} \in [0.0, 1.0]$: Point score for matched brand, RAM capacity, SSD size, and display technology.
- $M_{\text{use\_case}} \in [0.5, 1.0]$: Matching tag presence for coding, gaming, student, productivity, or fitness.
- $B_{\text{rating}} \in [0.0, 0.05]$: Rating credibility bonus for highly-rated items.
