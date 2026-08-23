# 🏗️ SmartCart AI-RAG Architecture

This document provides a detailed overview of the system architecture, component interactions, and data flows within the **SmartCart AI-RAG** platform.

---

## 1. High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  USER / BROWSER                                   |
|  - Ask SmartCart AI Search (Telugu / Roman Telugu / English)                      |
|  - Instant Product Recommendations & Grounded WHY Badges                          |
|  - Side-by-Side Comparison Matrix with AI Insights                                |
|  - Exact-Match Availability Alerts Subscription                                   |
+------------------------------------------+----------------------------------------+
                                           |
                                           | HTTP / JSON (REST API)
                                           v
+-----------------------------------------------------------------------------------+
|                        FASTAPI ASYNCHRONOUS BACKEND LAYER                         |
|  - CORS Middleware & Request Sanitization                                         |
|  - Route Handlers (/assistant, /search, /products, /compare, /cart, /subscribe)   |
+-------------------+---------------------------------------+-----------------------+
                    |                                       |
                    v                                       v
+-----------------------------------+   +-------------------------------------------+
|    MULTILINGUAL NLP NORMALIZER    |   |         HYBRID RETRIEVAL ENGINE           |
| - Telugu Concept Dictionary       |   | - FastEmbed (BAAI/bge-small-en-v1.5)      |
| - Price Bounds & Regex Extractor  |   | - Qdrant Vector DB (Dense 384d Vectors)   |
| - Strict Constraints Extractor    |   | - SQLite Relational Hydration             |
|   (RAM, SSD, Display, Brands)     |   | - 3-Level Graceful Budget Fallbacks       |
+-------------------+---------------+   +-------------------+-----------------------+
                    |                                       |
                    +-------------------+-------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                      DETERMINISTIC MULTI-FACTOR RANKING ENGINE                    |
|  Score = 0.30*Semantic + 0.20*Category + 0.20*Budget + 0.15*Specs + 0.15*Use-Case |
|  - Splits candidates into GROUP A (Direct Matches) & GROUP B (Alternatives)       |
|  - Calculates Over-Budget penalty & generates grounded why_recommended strings    |
+---------------------------------------+-------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                   OPENROUTER MULTI-MODEL FAILOVER LLM ENGINE                      |
|  - Primary: openrouter/auto                                                       |
|  - Fallback 1: google/gemini-2.0-flash-exp:free                                   |
|  - Fallback 2: meta-llama/llama-3.3-70b-instruct:free                             |
|  - Fallback 3: qwen/qwen-2.5-72b-instruct:free                                    |
|  - Ground Truth Telugu Script (తెలుగు లిపి) with Technical English Specs          |
+-----------------------------------------------------------------------------------+
```

---

## 2. Component Details

### A. Frontend Layer (Next.js 14 / React 19)
- **Framework**: Next.js App Router with TypeScript.
- **Styling**: Vanilla CSS design tokens in `app/globals.css` with responsive fluid grid.
- **Client State**: Local state management with reactive cart sessions, wishlist, comparison list, and language toggles.
- **Key Modules**:
  - `app/page.tsx`: Core application interface orchestrating AI search, product cards, category exploration, cart drawer, compare modal, and order history.
  - `lib/api.ts`: Typed asynchronous HTTP client communicating with FastAPI endpoints.

### B. Backend API Layer (FastAPI)
- **Framework**: FastAPI (Python 3.13) with Pydantic V2 validation and asynchronous route execution.
- **API Routers**:
  - `/api/v1/assistant/chat`: Orchestrates end-to-end shopping AI chat, candidate retrieval, ranking, dual product group assignment, and grounded LLM generation.
  - `/api/v1/search`: Hybrid semantic vector search endpoint.
  - `/api/v1/compare/insights`: Generates AI comparative analysis between selected products.
  - `/api/v1/subscribe`: Registers price/specification availability alert subscriptions.
  - `/api/v1/products`: Product catalog listing, category filtering, and product detail queries.
  - `/api/v1/cart`: Session-based shopping cart management.
  - `/api/v1/orders`: Order placement and tracking.
  - `/api/v1/health`: System health and vector index diagnostic endpoint.

### C. Vector Retrieval & RAG Pipeline (Qdrant + FastEmbed)
- **Embedding Model**: `BAAI/bge-small-en-v1.5` generating 384-dimensional dense vector embeddings.
- **Vector DB**: Qdrant running in embedded local storage mode (`backend/qdrant_storage`) or via standalone Qdrant server.
- **Catalog Indexing**: Auto-indexes all 67 product entries with rich contextual text including name, brand, category, subcategory, detailed specs, use cases, and feature tags.

### D. Relational Data Layer (SQLite + SQLAlchemy)
- **Database**: SQLite (`backend/smartcart.db`) managed through SQLAlchemy ORM.
- **Models**:
  - `ProductModel`: Catalog products with pricing, ratings, specs (JSON), tags (JSON), and stock.
  - `CategoryModel`: Category hierarchy and metadata.
  - `CartItemModel`: User cart items linked by session ID.
  - `WishlistItemModel`: Wishlist items linked by session ID.
  - `OrderModel`: Historical orders and order status.
  - `SubscriptionModel`: Availability alerts with structured constraints (Category, Max Price, RAM, Storage, Display).

---

## 3. Data Flow for a User Shopping Query

1. **User Submission**: The customer enters a query (e.g., `"naku 60000 lopu 16GB RAM laptop kavali"`).
2. **Intent & Constraint Extraction**:
   - Language is identified as Telugu (`telugu`).
   - Category mapped to `Electronics -> Laptops`.
   - Max price set to `60,000`.
   - RAM parsed as `16GB RAM`.
3. **Candidate Vector Retrieval**:
   - FastEmbed generates vector for `"coding laptop 16GB RAM"`.
   - Qdrant queries cosine distance filtered by Category `Laptops`.
4. **Fallback & Budget Evaluation**:
   - If products exist within ₹60k $\to$ **Level 1 (EXACT_MATCH)**.
   - If no products within ₹60k $\to$ **Level 2 (NO_EXACT_BUT_NEARBY)** expands budget up to +20% with penalty.
5. **Deterministic Ranking**:
   - Multi-factor scoring ranks candidates and assigns grounded `why_recommended` justifications.
6. **Product Group Assignment**:
   - **Group A (Direct Matches)**: Exact budget and spec matches.
   - **Group B (Related Alternatives)**: Near-budget picks.
7. **Bilingual LLM Synthesis**:
   - OpenRouter generates conversational response in Telugu script with technical specifications in English.
8. **UI Rendering**:
   - Response text, Group A cards, Group B cards, and Availability Alert CTA render simultaneously.
