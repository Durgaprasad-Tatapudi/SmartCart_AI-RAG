# 🚀 SmartCart AI-RAG Setup Guide

This guide walks you through setting up and running **SmartCart AI-RAG** locally from source.

---

## 1. Prerequisites

Ensure you have the following installed on your system:
- **Node.js**: `v18.17.0` or later (Node 20+ recommended)
- **Python**: `3.11`, `3.12`, or `3.13`
- **Git**: For cloning and repository management
- **OpenRouter API Key**: A valid API key from [openrouter.ai](https://openrouter.ai/keys)

---

## 2. Clone the Repository

```bash
git clone https://github.com/Durgaprasad-Tatapudi/SmartCart_AI-RAG.git
cd SmartCart_AI-RAG
```

---

## 3. Backend Setup & Configuration

### A. Create Virtual Environment
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
# Windows:
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
```

### B. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### C. Configure Environment Variables
Create a `.env` file in the `backend/` directory by copying `.env.example`:
```bash
# Windows:
copy .env.example .env

# Linux / macOS:
cp .env.example .env
```

Open `.env` and provide your OpenRouter API key:
```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-openrouter-key
OPENROUTER_MODEL=openrouter/auto
QDRANT_URL=http://localhost:6333
DATABASE_URL=sqlite:///./smartcart.db
FRONTEND_URL=http://localhost:3000
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
APP_ENV=development
```

> **Note on Vector DB**: You do **NOT** need to install or run external Qdrant. If `QDRANT_URL` is not reachable, the system automatically runs Qdrant in embedded local storage mode inside `backend/qdrant_storage`.

### D. Start the Backend Server
```bash
uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload
```

The backend server is now running:
- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Health Endpoint**: `http://localhost:8000/api/v1/health`

---

## 4. Frontend Setup & Configuration

### A. Install Node Modules
Open a new terminal window in the project root:
```bash
cd SmartCart_AI-RAG
npm install
```

### B. Configure Frontend Environment (Optional)
If running on a custom backend host, create a `.env.local` file in the project root:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### C. Start Next.js Development Server
```bash
npm run dev
```

The frontend application is now accessible at:
- **URL**: `http://localhost:3000`

---

## 5. Running Automated Tests

Run the complete 12-test automated verification suite:

```bash
cd backend
.venv\Scripts\python -u test_suite.py
```

This verifies:
1. Health check and vector database index status.
2. English and Telugu intent extraction.
3. Strict budget constraint enforcement.
4. Level 1 $\to$ 2 $\to$ 3 near-budget fallbacks.
5. Out-of-catalog responses with availability alert offers.
6. Side-by-side product comparison and AI insights generation.
7. Availability alert subscription creation.

---

## 6. Production Build (Frontend)

To build the Next.js frontend bundle for production deployment:
```bash
npm run build
npm run start
```
