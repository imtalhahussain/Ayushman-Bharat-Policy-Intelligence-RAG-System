# Ayushman Bharat Policy Intelligence RAG System
## A Production-Grade Retrieval-Augmented Generation (RAG) System for Healthcare Policy Intelligence

### This project is an end-to-end, production-ready RAG system designed to answer queries related to Ayushman Bharat, PM-JAY, and associated healthcare policies. Built with FastAPI, ChromaDB, SQLAlchemy, Sentence Transformers, and OpenAI GPT models, the system demonstrates complete AI engineering maturity — from data ingestion → vectorization → retrieval → generation → logging → deployment.

## Key Features
### 1. Intelligent RAG Pipeline
- PDF ingestion & cleanin
- Text chunking with metadata
- Vector embeddings using Sentence Transformers
- Semantic retrieval via Chroma Vector Store
- Optional re-ranking
- LLM-based response generation with citations
- Role-aware prompting (citizen / doctor / admin / policymaker)

### 2. End-to-End AI Engineering
#### This isn’t “just a chatbot.”
#### The project includes:
- Backend architecture
- Auth system foundation
- Database schema
- Feedback loop
- Evaluation engine
- Deployment-ready Dockerfile
- Modular codebase following real company patterns

### 3. Authentication & Role System
#### (Pluggable with JWT + DB, foundation already added)

#### Supports future roles:
- Citizen
- Doctor
- Hospital Admin
- Policy Maker

#### Each role influences:
- Retrieval filters
- Prompt templates
- Allowed actions

### 4. Document Intelligence
#### Stores:

- PDF metadata
- Document type
- Effective date
- Chunk-level embeddings
- Source citations in answers

### 5. Evaluation Framework (LLM-as-Judge)
#### Includes:

- Custom evaluation dataset eval_qa.csv
- Automatic RAG scoring
- Answer correctness
- Hallucination detection
- Retrieval quality (Recall@k, MRR)

### 6. FastAPI API Layer
#### API endpoints:
| Route       | Description                     |
| ----------- | ------------------------------- |
| `/chat/ask` | Main RAG endpoint               |
| `/auth/*`   | Signup/Login (foundation added) |
| `/admin/*`  | Upload PDFs, reindex docs       |
| `/health`   | Basic API health                |
| `/ready`    | Readiness probe for production  |

### 7. SQLAlchemy Database (Postgres-ready)
#### Models included:

- User
- Conversation
- Message
- Document
- Chunk
- RetrievalLog

#### Everything is wired with:

- Dependency injection (get_db)
- Session management
- Future ORM CRUD services

### 8. Deployable Architecture
#### Ready for:

- Docker
- Docker Compose
- Railway / Render / AWS ECS
- CI/CD via GitHub Actions

### Tech Stack
#### Backend: FastAPI
#### Vector Store: ChromaDB
#### Embeddings: Sentence Transformers
#### LLM: GPT-4o Mini (or any OpenAI model)
#### Database: SQLite (dev) → PostgreSQL (production)
#### Auth: JWT (foundation)
#### Deployment: Docker
#### Evaluation: LLM-as-Judge framework
#### Logging: Structured JSON Logging

## Project Structure
backend/
├─ app/
│  ├─ main.py                  # FastAPI entrypoint
│  ├─ config.py                # Env vars (OpenAI, JWT)
│  ├─ dependencies.py          # get_db & shared objects
│  ├─ logging_config.py        # JSON logging
│  │
│  ├─ api/
│  │  ├─ routes_chat.py        # /chat/ask + RAG API
│  │  ├─ routes_admin.py       # Upload PDFs, ingestion
│  │  ├─ routes_auth.py        # Signup/Login (stub)
│  │  └─ routes_health.py      # /health, /ready
│  │
│  ├─ db/
│  │  ├─ base.py               # ORM Base
│  │  ├─ session.py            # Engine + SessionLocal
│  │  ├─ models.py             # User, Document, etc.
│  │  └─ init_db.py            # Create tables
│  │
│  ├─ schemas/
│  │  ├─ chat.py               # ChatRequest/Response
│  │  ├─ auth.py               # JWT schemas
│  │  ├─ documents.py          # PDF metadata
│  │  └─ feedback.py           # Feedback logging
│  │
│  ├─ services/
│  │  ├─ auth_service.py       # Signup + hashing
│  │  ├─ security.py           # JWT + hashing utilities
│  │  ├─ document_service.py   # Store PDF metadata
│  │  └─ feedback_service.py   # Save ratings
│  │
│  ├─ rag/
│  │  ├─ ingest.py             # PDF → chunks → embeddings
│  │  ├─ clean_text.py         # Text normalization
│  │  ├─ chunk_text.py         # Chunking logic
│  │  ├─ vector_store.py       # Chroma client + queries
│  │  ├─ retrieve.py           # Semantic search
│  │  ├─ prompts.py            # Role-aware prompts
│  │  ├─ generate.py           # LLM answer generation
│  │  └─ pipeline.py           # Full RAG pipeline
│  │
│  └─ eval/
│     ├─ eval_config.py
│     ├─ eval_dataset_loader.py
│     ├─ eval_runner.py
│     └─ judge_llm.py
│
└─ Dockerfile

## Setup Instructions
### 1. Clone the repo
#### git clone https://github.com/<your-username>/<repo-name>.git
#### cd <repo-name>

### 2. Create environment
#### python -m venv .venv
#### .\.venv\Scripts\activate

### 3. Create .env
#### OPENAI_API_KEY=xxxx
#### JWT_SECRET=mysecret123

### 4. Run DB init
#### python -m backend.app.db.init_db

### 5. Start FastAPI
#### uvicorn backend.app.main:app --reload

### 6.Test in Swagger UI
#### http://127.0.0.1:8000/docs

## RAG Pipeline Overview
flowchart TD
    A[PDFs] --> B[Clean Text]
    B --> C[Chunking + Metadata]
    C --> D[Embeddings]
    D --> E[Chroma Vector Store]
    E --> F[Retriever]
    F --> G[Prompt Builder]
    G --> H[LLM - GPT]
    H --> I[Final Answer + Citations]

## Upcoming Features (Roadmap)
## Next Milestone
- JWT-based signup/login with PostgreSQL
- Password hashing
- JWT token issuing
- Role-based access control
- /auth/me endpoint

## Future Milestones

- Admin PDF dashboard
- Retrieval logging + feedback loop
- Multi-role prompt conditioning
- Reranking (Cross Encoder)
- Frontend chat UI (Next.js)
- Cloud deployment (Railway / Render)
- CI/CD pipeline
- Policy coverage expansion
- Evaluation dashboard

## Why This Project Matters
### This system demonstrates full-stack AI engineering, including:

- Real-world backend architecture
- RAG retrieval optimization
- Prompt engineering
- Vector search
- LLM evaluation
- Structured databases
- API design
- Modular services
- Deployment-readiness