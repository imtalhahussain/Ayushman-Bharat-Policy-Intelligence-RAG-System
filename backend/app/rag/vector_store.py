# backend/app/rag/vector_store.py

import os
import chromadb
from sentence_transformers import SentenceTransformer

# Absolute project root: rag -> app -> backend -> ROOT
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma")
COLLECTION_NAME = "ayushman_policies"

os.makedirs(CHROMA_DIR, exist_ok=True)

print(f"[vector_store] BASE_DIR   = {BASE_DIR}")
print(f"[vector_store] CHROMA_DIR = {CHROMA_DIR}")

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL)


def get_chroma_client():
    """
    Persistent Chroma client. Data stored on disk under CHROMA_DIR.
    No client.persist() needed in this API.
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client


def get_or_create_collection(client):
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def embed_texts(texts):
    return embedder.encode(texts).tolist()
