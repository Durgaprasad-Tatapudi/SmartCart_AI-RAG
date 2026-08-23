# SmartCart AI — Backend

AI-powered multilingual shopping assistant backend built with **FastAPI**, **Qdrant Vector Database**, **OpenRouter LLM**, and **SQLite**.

---

## 🏗 Architecture Overview

```
                      USER QUERY
                          │
                          ▼
                   FastAPI Backend
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    SQLite DB        Qdrant DB      OpenRouter LLM
   (Relational)      (Vector DB)     (Language NLU)
   • Products        • Dense Embed   • Intent Extraction
   • Cart            • Semantic      • Grounded Explanations
   • Orders            Retrieval     • Multilingual Chat
   • Categories      • Cosine sim
          │               │               │
          └───────────────┼───────────────┘
                          │
                          ▼
               Deterministic Ranking
                          │
                          ▼
                 Frontend JSON API
```

---

## 🚀 Quick Setup & Run

### Prerequisites:
- Python 3.11+
- (Optional) Docker for Qdrant server

### 1. Create Virtual Environment and Install Dependencies:

```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment:

Copy `.env.example` to `.env` and configure your keys:

```bash
cp .env.example .env
```

Set `OPENROUTER_API_KEY` (if available) for live LLM reasoning, or leave blank to use the built-in deterministic offline fallback engine.

### 3. Seed Database & Index Vectors:

```bash
python scripts/seed_database.py
python scripts/index_products.py
```

### 4. Run Backend Server:

```bash
uvicorn app.main:app --reload --port 8000
```

- API Base URL: `http://localhost:8000/api/v1`
- Interactive Swagger Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

---

## 🧪 Run Automated Tests:

```bash
pytest tests/
```

---

## 🐳 Docker Deployment:

To run both Qdrant and FastAPI in containers:

```bash
docker compose up -d
```
