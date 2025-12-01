## Ayushman Bharat Policy Intelligence RAG System

A complete end-to-end Retrieval-Augmented Generation (RAG) platform for answering questions about Ayushman Bharat / PM-JAY policies using official government PDFs.

⭐ Overview

This project is a fully built production-ready RAG backend, designed to help citizens, doctors, hospital administrators, and policymakers get accurate, citation-based answers from official Ayushman Bharat policy documents.

It showcases real-world AI engineering skills across:
-> Data ingestion
-> Text cleaning & chunking
-> Vector embeddings
-> Chroma vector database
-> FastAPI backend
-> LLM-generated answers
-> Document citation
-> Role-aware prompting (upcoming)
-> Evaluation framework (upcoming)
-> Frontend UI (upcoming)

🔥 Key Features
🧠 1. End-to-End RAG Pipeline

Extracts text from PDFs using PyMuPDF

Cleans & normalizes text

Splits into high-quality semantic chunks

Generates embeddings using sentence-transformers

Stores them in a Chroma vector database

Retrieves top-k relevant chunks using semantic search

🤖 2. LLM-Powered Answers

LLM generates correct, grounded answers

Uses retrieved policy text as trusted context

Avoids hallucinations

Always returns exact source snippets for transparency

⚖️ 3. Policy-Specific Intelligence

Built for Ayushman Bharat / PM-JAY

Designed for real-world policy queries:

Coverage

Eligibility

Packages

Hospital roles

Infrastructure guidelines

Beneficiary support

🎭 4. Role-Aware RAG (Upcoming)

Citizen mode

Doctor mode

Hospital admin mode

Policy maker mode

Each role will get custom prompting and retrieval behavior.

📊 5. Evaluation Framework (Upcoming)

CSV of Q&A benchmark

LLM-as-judge scoring

Hallucination detection

Retrieval quality tracking

💬 6. API Ready

FastAPI backend

/chat/ask endpoint

Fully JSON based

Swagger documentation included

🏗️ Project Architecture
Ayushman Bharat Policy Intelligence RAG System/
│
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI app entry
│       │
│       ├── api/
│       │   └── routes_chat.py      # /chat/ask endpoint
│       │
│       ├── schemas/
│       │   └── chat.py             # Request/Response Pydantic models
│       │
│       ├── rag/
│       │   ├── ingest.py           # Build vector store
│       │   ├── retrieve.py         # Chroma top-k retrieval
│       │   ├── pipeline.py         # LLM RAG logic
│       │   ├── prompts.py          # RAG prompts
│       │   ├── llm_client.py       # OpenAI wrapper
│       │   └── vector_store.py     # Chroma client setup
│       │
│       └── config.py           # Loads .env (API keys)
│
├── data/
│   ├── pdfs/                       # Policy PDFs (ignored in git)
│   ├── cleaned/                    # Cleaned text
│   ├── extracted/                  # Raw extracted pages
│   └── chunks/                     # chunks.jsonl
│
├── scripts/
│   └── load_pdfs.py                # PDF → text extraction
│
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Getting Started
1️⃣ Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2️⃣ Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your .env file (NOT committed)

Create .env in the project root:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

5️⃣ Add PDFs

Place official Ayushman Bharat / PM-JAY policy PDFs inside:

data/pdfs/

6️⃣ Run the pipeline
python scripts/load_pdfs.py
python backend/app/rag/clean_text.py
python backend/app/rag/chunk_text.py
python -m backend.app.rag.ingest

7️⃣ Start the FastAPI server
uvicorn backend.app.main:app --reload


Visit Swagger:
👉 http://127.0.0.1:8000/docs

🔌 Using the /chat/ask API

Request:

{
  "query": "what is ayushman bharat pradhan mantri jan arogya yojana",
  "top_k": 3
}


Response:

{
  "answer": "Ayushman Bharat PM-JAY is ...",
  "sources": [
    {
      "source": "policy10",
      "page_start": 1,
      "page_end": 1,
      "text": "..."
    }
  ]
}

🧭 Roadmap (40 LPA Version)
✅ Completed

PDF ingestion pipeline

Text cleaning

Chunking

Vector embeddings

Chroma storage

Semantic retrieval

LLM answering

API endpoint

🔜 Coming Next (high-impact)

 Role-based prompting

 Evaluation framework

 Hallucination scoring

 Frontend chat UI

 Docker deployment

 Model monitoring

🥇 Why this Project is 40-LPA Ready

Full-stack RAG implemented from scratch

Grasps ingestion → embedding → retrieval → generation pipeline

Uses production technologies (Chroma, FastAPI, LLM APIs)

Clean modular architecture

Configurable, extensible code

Demonstrates real-world AI engineering practices

Perfect for interviews + portfolio

📄 License

MIT License

👨‍💻 Developed by

Talha, Founder of Arlow Craft
AI + RAG Developer | Building production-grade AI systems
