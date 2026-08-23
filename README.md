# 🛒 SmartCart – Multilingual AI-Powered Shopping Assistant

SmartCart is a next-generation, AI-first e-commerce shopping consultant built with **Next.js 14**, **FastAPI**, **Qdrant Vector Database**, **FastEmbed**, and **OpenRouter LLMs**.

Unlike traditional keyword-based search engines that fail on natural language queries, SmartCart acts as an intelligent, human-like sales consultant. It understands conversational queries in **English**, **Telugu script (తెలుగు లిపి)**, and **Telugu transliteration (Roman Telugu)**, extracts structured shopping specifications (Budget, RAM, Storage, Processor, Display, Brand, Use-case), performs hybrid semantic vector search, ranks candidates deterministically, and provides personalized, grounded explanations.

---

## 📸 System Overview & Capabilities

```
User Query (Telugu / Roman Telugu / English)
                  │
                  ▼
   ┌────────────────────────────────────────┐
   │    Query Normalization & Parsing       │
   │  - Language Detection (EN / TE)        │
   │  - Price & Constraint Extraction       │
   │  - Brand & Spec Identification         │
   │  - Strict vs Flexible Requirements     │
   └──────────────────┬─────────────────────┘
                      │
                      ▼
   ┌────────────────────────────────────────┐
   │    Hybrid Retrieval Engine             │
   │  - Dense Semantic Vector Search        │
   │    (FastEmbed BAAI/bge-small-en-v1.5)  │
   │  - Qdrant Vector Collection            │
   │  - SQLite Relational Hydration         │
   │  - Level 1 ➔ 2 ➔ 3 Fallback Search    │
   └──────────────────┬─────────────────────┘
                      │
                      ▼
   ┌────────────────────────────────────────┐
   │  Deterministic Multi-Factor Ranking    │
   │  - Semantic Relevance (30%)            │
   │  - Category & Subcategory Match (20%)  │
   │  - Budget Fit & Over-Budget Curve (20%)│
   │  - Spec (RAM/SSD/Display) Match (15%)  │
   │  - Use-case & Rating Alignment (15%)   │
   └──────────────────┬─────────────────────┘
                      │
                      ▼
   ┌────────────────────────────────────────┐
   │  Grounded Multilingual Generation      │
   │  - OpenRouter Auto / Multi-Model LLM   │
   │  - Natural Telugu Script (తెలుగు లిపి) │
   │  - Per-Product WHY Explanations        │
   │  - Group A (Exact) & Group B (Related) │
   └──────────────────┬─────────────────────┘
                      │
                      ▼
            Interactive UI Delivery
     (AI Message + Instant Product Cards)
```

---

## ✨ Key Features

### 1. 🤖 Intelligent Conversational Shopping Assistant
- **Zero Extra Clicks**: Users receive the AI sales response and clickable product cards simultaneously.
- **Bilingual Fluency**: Seamlessly switches between English and pure Telugu script (**తెలుగు లిపి**) with hardware specifications displayed in clear technical English (e.g., `16GB RAM + 512GB SSD`).
- **Grounded "WHY Recommended" Justifications**: Every recommended item displays a grounded reason explaining why it fits the user's specific use-case, budget, and specs.

### 2. 🎯 Two-Group Product Partitioning
- **GROUP A (Direct Matches / మీకు సరిపోయే ఎంపికలు)**: Products that strictly satisfy all user constraints.
- **GROUP B (Related Alternatives / మీకు దగ్గరగా ఉన్న ఎంపికలు)**: Near-budget or close-alternative products clearly labeled with `+₹X above budget` badges when exact budget matches are limited.

### 3. 🛡️ 3-Level Graceful Budget Fallback
- **Level 1 (Strict Budget)**: Searches strictly within the specified price limit.
- **Level 2 (Near-Budget Relaxation)**: If no items exist within budget, expands to nearby products up to +20% to +50% above budget with clear cost difference badges.
- **Level 3 (Honest Out-of-Catalog Explanation & Alerts)**: If an item or category is completely unavailable, the assistant transparently explains the limitation and offers an automated availability alert.

### 4. 🔔 Availability & Exact-Match Alert Subscriptions
- Non-intrusive alert CTA whenever an exact specification or out-of-catalog item is requested.
- Captures prefilled structured constraints (Category, Max Price, RAM, Storage, Display) and persists them in SQLite for automated user notifications.

### 5. ⚖️ Side-by-Side Product Comparison & AI Insights
- Compare up to 4 products in a unified side-by-side spec sheet.
- **AI Comparison Insights**: Generates a comparative analysis highlighting which product is better for specific requirements.

### 6. 🛍️ End-to-End E-Commerce Flow
- Interactive Cart drawer with quantity controls, subtotal, taxes, discount calculations, and free shipping progress.
- Wishlist management and real-time Orders lookup.

---

## 🛠️ Technology Stack

| Layer | Technologies Used | Description |
| :--- | :--- | :--- |
| **Frontend** | Next.js 14 (App Router), React 19, TypeScript, Vanilla CSS Tokens, Lucide Icons | Responsive, state-of-the-art UI with dark/light variables and instant transitions |
| **Backend** | FastAPI, Python 3.13, Uvicorn, Pydantic V2 | High-performance asynchronous REST API backend |
| **Vector DB** | Qdrant (Embedded Local Storage / Client), FastEmbed | Dense semantic vector search using `BAAI/bge-small-en-v1.5` (384 dimensions) |
| **Relational DB** | SQLite, SQLAlchemy ORM | Local catalog persistence, orders, cart sessions, wishlist, and alert subscriptions |
| **AI / LLM** | OpenRouter API (`openrouter/auto`, `meta-llama`, `google/gemini`, `qwen`) | Multi-model failover engine for fast, grounded bilingual conversational responses |

---

## 📂 Project Structure

```
smart-cart-ai/
├── app/                              # Next.js 14 App Router
│   ├── globals.css                   # Unified CSS design tokens, typography, and classes
│   ├── layout.tsx                    # Root layout with fonts & metadata
│   └── page.tsx                      # Main single-page application & all UI modals
├── components/                       # Frontend UI components
│   ├── logo.tsx                      # SmartCart SVG Brand Logo
│   └── ui/                           # Reusable UI primitives
├── lib/
│   └── api.ts                        # TypeScript API client & data interfaces
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/                      # REST API Endpoints
│   │   │   ├── assistant.py          # POST /api/v1/assistant/chat (AI Chat & Recommendations)
│   │   │   ├── compare.py            # POST /api/v1/compare/insights & product comparisons
│   │   │   ├── search.py             # POST /api/v1/search (Vector + Hybrid search)
│   │   │   ├── products.py           # GET /api/v1/products (Catalog CRUD & filtering)
│   │   │   ├── categories.py         # GET /api/v1/categories
│   │   │   ├── cart.py               # Cart operations (/api/v1/cart)
│   │   │   ├── orders.py             # Orders lookup & creation (/api/v1/orders)
│   │   │   ├── wishlist.py           # Wishlist management (/api/v1/wishlist)
│   │   │   ├── subscription.py       # POST /api/v1/subscribe (Availability alerts)
│   │   │   └── health.py             # GET /api/v1/health
│   │   ├── core/                     # Configuration, logging & security sanitization
│   │   ├── db/                       # SQLAlchemy models, SQLite engine & seed data
│   │   ├── schemas/                  # Pydantic request & response models
│   │   ├── services/                 # Core AI, Ranking, Embedding & Vector Services
│   │   │   ├── embedding_service.py  # FastEmbed model wrapper
│   │   │   ├── vector_service.py     # Qdrant client & indexing
│   │   │   ├── ranking_service.py    # Multi-factor deterministic ranking formula
│   │   │   ├── search_service.py     # Level 1->2->3 hybrid search coordinator
│   │   │   └── llm_service.py        # OpenRouter multi-model LLM engine & Telugu prompts
│   │   ├── utils/
│   │   │   └── normalization.py      # Multilingual Telugu/English query parsing & NLP
│   │   └── main.py                   # FastAPI application entrypoint & lifecycle
│   ├── qdrant_storage/               # Local embedded Qdrant vector database storage
│   ├── smartcart.db                  # Local SQLite relational database file
│   ├── test_suite.py                 # Automated 12-test suite for end-to-end verification
│   ├── requirements.txt              # Python backend dependencies
│   ├── .env.example                  # Environment variable template
│   └── .env                          # Local environment configuration
├── package.json                      # Frontend Node.js dependencies
└── README.md                         # Project documentation
```

---

## ⚙️ Installation & Setup Guide

### 1. Prerequisites
- **Node.js** (v18.17+ or v20+)
- **Python** (v3.11, v3.12, or v3.13)
- **OpenRouter API Key** (Get free/paid key from [openrouter.ai](https://openrouter.ai))

---

### 2. Backend Setup

1. **Navigate to the backend folder**:
   ```bash
   cd backend
   ```

2. **Create and activate a Python virtual environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the `backend/` directory:
   ```env
   # OpenRouter LLM Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=openrouter/auto

   # Qdrant Vector Database (Embedded storage is used automatically if URL is not reachable)
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=
   QDRANT_COLLECTION=smartcart_products

   # SQLite Database
   DATABASE_URL=sqlite:///./smartcart.db

   # Frontend Application Origin for CORS
   FRONTEND_URL=http://localhost:3000

   # Multilingual Embedding Model
   EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

   # Environment
   APP_ENV=development
   ```

5. **Start the Backend Server**:
   ```bash
   uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload
   ```
   - API Docs (Swagger): `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/v1/health`

---

### 3. Frontend Setup

1. **Open a new terminal in the project root**:
   ```bash
   cd smart-cart-ai
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Run the Next.js development server**:
   ```bash
   npm run dev
   ```
   - Open your browser at `http://localhost:3000`

---

## 🧪 Automated Test Suite

A comprehensive 12-test suite is provided to verify all core AI functionalities, vector search, budget fallbacks, multilingual script generation, and compare insights:

```bash
cd backend
.venv\Scripts\python -u test_suite.py
```

### Verified Test Scenarios:
1. **Coding laptop under ₹60,000 (Telugu Transliteration)** $\to$ Exact budget match with why recommended points.
2. **Best earbuds under ₹5,000 (English)** $\to$ Verified within-budget picks.
3. **Laptop under ₹15,000 (Near-Budget Fallback)** $\to$ Returns near-budget picks (`+₹4,999 above budget`) and activates the subscription alert offer.
4. **Out-of-Catalog Request (DSLR Camera)** $\to$ Returns 0 products, transparent explanation, and alert CTA.
5. **Pure Telugu Script Query (నాకు ₹60,000 లోపు coding laptop కావాలి)** $\to$ Natural Telugu script response.
6. **Semantic Natural Search without Price** $\to$ Accurately matches coding laptops.
7. **Hard Specification Constraints (16GB RAM + ₹80k)** $\to$ Strictly filters and boosts 16GB models.
8. **Multi-Product Comparison** $\to$ Returns structured comparison attributes.
9. **AI Comparison Insights** $\to$ Generates grounded comparative explanations.
10. **Bilingual Switch (English $\leftrightarrow$ Telugu)** $\to$ Validates language consistency.
11. **Availability Subscription API** $\to$ Saves structured alerts to SQLite.
12. **Unsupported Category Check (Washing Machine)** $\to$ Graceful out-of-scope response.

---

## 📡 API Reference Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/assistant/chat` | AI Shopping Consultant chat (Intent, Vector Search, Dual Product Groups, Multilingual Response) |
| `POST` | `/api/v1/search` | Direct Hybrid semantic + keyword search with fallback |
| `POST` | `/api/v1/compare/insights` | Generates AI comparative analysis between selected products |
| `POST` | `/api/v1/subscribe` | Registers structured product availability alerts |
| `GET` | `/api/v1/products` | Paginated product listing with category/price filters |
| `GET` | `/api/v1/categories` | Returns all available categories and subcategories |
| `GET` | `/api/v1/cart/{session_id}` | Retrieves items in user cart |
| `POST` | `/api/v1/cart/{session_id}/items` | Adds a product to cart |
| `GET` | `/api/v1/orders/{session_id}` | Retrieves order history for a session |
| `GET` | `/api/v1/health` | Health and vector index status check |

---

## 🧮 Multi-Factor Ranking Formula

Candidate products are ranked deterministically using the following formula:

$$\text{Final Score} = 0.30 \cdot S_{\text{semantic}} + 0.20 \cdot M_{\text{category}} + 0.20 \cdot F_{\text{budget}} + 0.15 \cdot M_{\text{specs}} + 0.15 \cdot M_{\text{use\_case}} + B_{\text{rating}}$$

- **$S_{\text{semantic}}$**: Cosine similarity from FastEmbed 384d vectors.
- **$M_{\text{category}}$**: Exact category and subcategory match score.
- **$F_{\text{budget}}$**: $1.0$ if $\text{Price} \le \text{Budget}$; penalized smoothly if within near-budget threshold.
- **$M_{\text{specs}}$**: Matches RAM (e.g. 16GB), Storage (e.g. 512GB/1TB SSD), Display (OLED/4K), and Brands.
- **$M_{\text{use\_case}}$**: Matches tags for coding, gaming, student, office, running, etc.
- **$B_{\text{rating}}$**: Bonus for products rated $\ge 4.5\star$ with high review counts.

---

## 📄 License & Credits
Built for **SmartCart AI**. Powered by Next.js, FastAPI, Qdrant, FastEmbed, and OpenRouter.
